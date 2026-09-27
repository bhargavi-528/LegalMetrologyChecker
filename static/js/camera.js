let stream = null;
let currentFacingMode = "environment";
let torchEnabled = false;

const video = document.getElementById("camera");
const canvas = document.getElementById("canvas");

const startCameraButton =
    document.getElementById("startCamera");

const captureButton =
    document.getElementById("captureButton");

const torchButton =
    document.getElementById("torchButton");

const switchCameraButton =
    document.getElementById("switchCamera");

const cameraPlaceholder =
    document.getElementById("cameraPlaceholder");


async function startCamera() {

    stopCamera();

    try {

        stream = await navigator.mediaDevices.getUserMedia({

            video: {
                facingMode: {
                    ideal: currentFacingMode
                },
                width: {
                    ideal: 1920
                },
                height: {
                    ideal: 1080
                }
            },

            audio: false
        });


        video.srcObject = stream;

        cameraPlaceholder.style.display =
            "none";

        captureButton.disabled = false;
        switchCameraButton.disabled = false;

        const track =
            stream.getVideoTracks()[0];

        const capabilities =
            track.getCapabilities();

        if (capabilities.torch) {

            torchButton.disabled = false;

            torchButton.textContent =
                "🔦 Torch OFF";

        } else {

            torchButton.disabled = true;

            torchButton.textContent =
                "🔦 Not Supported";

        }

    } catch (error) {

        console.error(error);

        alert(
            "Camera access failed. Please allow camera permission or use Upload Image."
        );

    }
}


async function toggleTorch() {

    if (!stream) {
        return;
    }

    const track =
        stream.getVideoTracks()[0];

    const capabilities =
        track.getCapabilities();

    if (!capabilities.torch) {
        return;
    }

    torchEnabled =
        !torchEnabled;

    try {

        await track.applyConstraints({

            advanced: [
                {
                    torch: torchEnabled
                }
            ]

        });

        torchButton.textContent =
            torchEnabled
                ? "🔦 Torch ON"
                : "🔦 Torch OFF";

    } catch (error) {

        console.error(
            "Torch error:",
            error
        );

    }
}


function switchCamera() {

    currentFacingMode =
        currentFacingMode === "environment"
            ? "user"
            : "environment";

    startCamera();
}


function captureImage() {

    if (!stream) {
        return null;
    }

    const width =
        video.videoWidth;

    const height =
        video.videoHeight;

    canvas.width = width;
    canvas.height = height;

    const context =
        canvas.getContext("2d");

    context.drawImage(
        video,
        0,
        0,
        width,
        height
    );

    return canvas.toDataURL(
        "image/jpeg",
        0.95
    );
}


function stopCamera() {

    if (stream) {

        stream
            .getTracks()
            .forEach(track => {
                track.stop();
            });

        stream = null;
    }

    torchEnabled = false;
}


if (startCameraButton) {

    startCameraButton.addEventListener(
        "click",
        startCamera
    );

}


if (torchButton) {

    torchButton.addEventListener(
        "click",
        toggleTorch
    );

}


if (switchCameraButton) {

    switchCameraButton.addEventListener(
        "click",
        switchCamera
    );

}


if (captureButton) {

    captureButton.addEventListener(
        "click",
        () => {

            const image =
                captureImage();

            if (image) {

                window.processCapturedImage(
                    image
                );

            }

        }
    );

}