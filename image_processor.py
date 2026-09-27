import cv2
import numpy as np


def preprocess_image(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to read image.")

    # Resize
    height, width = image.shape[:2]

    scale = 2

    resized = cv2.resize(
        image,
        (width * scale, height * scale),
        interpolation=cv2.INTER_CUBIC
    )

    # Grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # Noise reduction
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

    # Contrast enhancement
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(denoised)

    # Sharpen
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    sharpened = cv2.filter2D(
        enhanced,
        -1,
        kernel
    )

    return resized, sharpened