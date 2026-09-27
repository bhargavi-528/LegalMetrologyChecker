import cv2


def detect_color(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    avg_hue = float(hsv[:, :, 0].mean())
    avg_saturation = float(hsv[:, :, 1].mean())
    avg_value = float(hsv[:, :, 2].mean())

    if avg_saturation < 40 and avg_value > 180:
        color = "White / Light"
    elif avg_value < 70:
        color = "Black / Dark"
    elif avg_hue < 15 or avg_hue > 165:
        color = "Red"
    elif avg_hue < 35:
        color = "Yellow / Orange"
    elif avg_hue < 85:
        color = "Green"
    elif avg_hue < 130:
        color = "Blue"
    else:
        color = "Mixed / Other"

    return color


def detect_shape(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return "Unknown"

    largest = max(contours, key=cv2.contourArea)

    area = float(cv2.contourArea(largest))

    if area < 1000:
        return "Unknown"

    perimeter = float(cv2.arcLength(largest, True))

    approx = cv2.approxPolyDP(
        largest,
        0.04 * perimeter,
        True
    )

    corners = int(len(approx))

    x, y, w, h = cv2.boundingRect(largest)

    w = int(w)
    h = int(h)

    ratio = float(w / h) if h != 0 else 0.0

    if corners == 4:
        if 0.85 <= ratio <= 1.15:
            return "Rectangular / Square"
        return "Rectangular"

    if corners > 4:
        return "Rounded / Irregular"

    return "Irregular"


def analyze_package(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not read image.")

    return {
        "color": str(detect_color(image)),
        "shape": str(detect_shape(image))
    }