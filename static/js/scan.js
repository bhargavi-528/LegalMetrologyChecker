const uploadButton =
    document.getElementById("uploadButton");

const imageUpload =
    document.getElementById("imageUpload");

const processing =
    document.getElementById("processing");

const errorBox =
    document.getElementById("errorBox");


uploadButton.addEventListener(
    "click",
    () => {
        imageUpload.click();
    }
);


imageUpload.addEventListener(
    "change",
    () => {

        if (
            imageUpload.files &&
            imageUpload.files.length > 0
        ) {

            uploadImage(
                imageUpload.files[0]
            );

        }

    }
);


window.processCapturedImage =
    function(dataUrl) {

        fetch(dataUrl)
            .then(response =>
                response.blob()
            )
            .then(blob => {

                const file =
                    new File(
                        [blob],
                        "camera_capture.jpg",
                        {
                            type: "image/jpeg"
                        }
                    );

                uploadImage(file);

            })
            .catch(error => {

                showError(
                    "Unable to process camera image."
                );

            });

    };


function uploadImage(file) {

    hideError();

    processing.hidden = false;

    const formData =
        new FormData();

    formData.append(
        "image",
        file
    );


    fetch(
        "/analyze",
        {
            method: "POST",
            body: formData
        }
    )

    .then(response =>
        response.json()
    )

    .then(data => {

        processing.hidden = true;

        if (!data.success) {

            showError(
                data.error ||
                "Analysis failed."
            );

            return;
        }

        window.location.href =
            "/report";

    })

    .catch(error => {

        processing.hidden = true;

        showError(
            "Something went wrong while analysing the image."
        );

        console.error(error);

    });

}


function showError(message) {

    errorBox.hidden = false;

    errorBox.textContent =
        message;

}


function hideError() {

    errorBox.hidden = true;

    errorBox.textContent =
        "";

}