import os
import uuid

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
    send_from_directory
)

from database import init_db, save_inspection, get_history
from ocr_engine import run_ocr
from extractor import extract_information
from rule_engine import check_rules
from visual_analyzer import analyze_package
from report_generator import create_report


app = Flask(__name__)
app.secret_key = "legal-metrology-demo-secret"

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("reports", exist_ok=True)

init_db()

latest_result = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan")
def scan():
    role = session.get("role", "Consumer")
    return render_template("scan.html", role=role)


@app.route("/set-role", methods=["POST"])
def set_role():
    session["role"] = request.form.get(
        "role",
        "Consumer"
    )
    return redirect(url_for("scan"))


@app.route("/analyze", methods=["POST"])
def analyze():

    global latest_result

    print("\n========== ANALYSIS STARTED ==========")

    if "image" not in request.files:
        print("ERROR: No image")

        return jsonify({
            "success": False,
            "error": "No image uploaded."
        }), 400

    image = request.files["image"]

    if image.filename == "":
        print("ERROR: Empty filename")

        return jsonify({
            "success": False,
            "error": "No image selected."
        }), 400

    extension = os.path.splitext(
        image.filename
    )[1].lower()

    allowed = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    ]

    if extension not in allowed:
        return jsonify({
            "success": False,
            "error": "Unsupported image format."
        }), 400

    filename = str(uuid.uuid4()) + extension

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    image.save(filepath)

    print(
        "Image saved:",
        filepath
    )

    try:

        print("1. Starting OCR...")

        ocr = run_ocr(filepath)

        print(
            "OCR finished. Text length:",
            len(ocr["text"])
        )


        print(
            "2. Extracting information..."
        )

        extracted = extract_information(
            ocr["text"]
        )

        print(
            "Extraction finished."
        )


        print(
            "3. Checking rules..."
        )

        compliance = check_rules(
            extracted
        )

        print(
            "Rules finished."
        )


        print(
            "4. Analysing package..."
        )

        visual = analyze_package(
            filepath
        )

        print(
            "Visual analysis finished."
        )


        result = {
            "success": True,

            "role": session.get(
                "role",
                "Consumer"
            ),

            "image": "/uploads/" + filename,

            "ocr": {
                "text": ocr["text"],
                "confidence": ocr["confidence"],
                "detections": ocr["results"]
            },

            "product": extracted,

            "compliance": compliance,

            "visual": visual
        }


        latest_result = result


        print("5. Saving inspection...")

        # Convert NumPy values to normal Python values
        import numpy as np

        def make_json_safe(obj):
            if isinstance(obj, dict):
                return {
                    key: make_json_safe(value)
                    for key, value in obj.items()
                }

            if isinstance(obj, list):
                return [
                    make_json_safe(value)
                    for value in obj
                ]

            if isinstance(obj, tuple):
                return [
                    make_json_safe(value)
                    for value in obj
                ]

            if isinstance(obj, np.integer):
                return int(obj)

            if isinstance(obj, np.floating):
                return float(obj)

            if isinstance(obj, np.ndarray):
                return obj.tolist()

            return obj


        result = make_json_safe(result)


        save_inspection(
            result["role"],
            extracted.get(
                "product_name",
                "Unknown"
            ),
            compliance["overall"],
            compliance["score"],
            result
        )


        print("Inspection saved successfully.")


        print(
            "6. Creating report..."
        )

        create_report(result)


        print(
            "========== ANALYSIS COMPLETE ==========\n"
        )

        return jsonify(result)


    except Exception as error:

        print(
            "\n!!!!!!!! ERROR !!!!!!!!"
        )

        print(error)

        print(
            "!!!!!!!!!!!!!!!!!!!!!!!\n"
        )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


@app.route("/report")
def report():
    return render_template(
        "report.html",
        result=latest_result
    )


@app.route("/history")
def history():

    records = get_history()

    return render_template(
        "history.html",
        records=records
    )


@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


if __name__ == "__main__":

    print("\n====================================")
    print(" Legal Metrology Compliance Checker")
    print("====================================")
    print("Open: http://127.0.0.1:5000\n")

    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000
    )