import easyocr
import cv2

_reader = None


def get_reader():
    global _reader

    if _reader is None:
        _reader = easyocr.Reader(
            ['en'],
            gpu=False,
            verbose=False
        )

    return _reader


def run_ocr(image_path):

    reader = get_reader()

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not read image.")

    # Resize only once
    height, width = image.shape[:2]

    if width < 1200:
        scale = 1200 / width
        image = cv2.resize(
            image,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_CUBIC
        )

    # ONE OCR pass first — much faster
    results = reader.readtext(
        image,
        detail=1,
        paragraph=False
    )

    detections = []

    for result in results:

        if len(result) >= 3:

            bbox = result[0]
            text = result[1].strip()
            confidence = float(result[2])

            if text:

                detections.append({
                    "text": text,
                    "confidence": round(confidence, 3),
                    "bbox": bbox
                })

    text = "\n".join(
        item["text"]
        for item in detections
    )

    if detections:

        avg_confidence = sum(
            item["confidence"]
            for item in detections
        ) / len(detections)

    else:

        avg_confidence = 0

    return {
        "text": text,
        "results": detections,
        "confidence": round(avg_confidence, 3)
    }