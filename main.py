import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from PIL import Image


# ============================================================
# PRETRAINED IMAGE CLASSIFICATION USING MOBILENETV2
# ============================================================


# Load the pretrained MobileNetV2 model
print("Loading MobileNetV2 model...")

model = tf.keras.applications.MobileNetV2(
    weights="imagenet"
)

print("Model loaded successfully!\n")


# Folder containing sample images
IMAGE_FOLDER = "sample_images"


# ============================================================
# IMAGE CLASSIFICATION FUNCTION
# ============================================================

def classify_image(image_path):

    # Open the image
    image = Image.open(image_path).convert("RGB")

    # Resize image to 224 x 224
    image = image.resize((224, 224))

    # Convert image to NumPy array
    image_array = np.array(image)

    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)

    # Preprocess image for MobileNetV2
    image_array = tf.keras.applications.mobilenet_v2.preprocess_input(
        image_array
    )

    # Make prediction
    predictions = model.predict(
        image_array,
        verbose=0
    )

    # Get top 3 predictions
    decoded_predictions = (
        tf.keras.applications.mobilenet_v2.decode_predictions(
            predictions,
            top=3
        )[0]
    )

    return image, decoded_predictions


# ============================================================
# FIND SAMPLE IMAGES
# ============================================================

image_files = [
    file for file in os.listdir(IMAGE_FOLDER)
    if file.lower().endswith(
        (".jpg", ".jpeg", ".png")
    )
]


# ============================================================
# CHECK FOR IMAGES
# ============================================================

if not image_files:

    print("No images found in the sample_images folder.")
    print("Please add JPG, JPEG, or PNG images.")

else:

    # Limit the display to 6 images
    image_files = image_files[:6]

    # Store classification results
    results = []


    # ========================================================
    # CLASSIFY EACH IMAGE
    # ========================================================

    for file in image_files:

        image_path = os.path.join(
            IMAGE_FOLDER,
            file
        )

        image, predictions = classify_image(
            image_path
        )

        # Get top prediction
        top_label = predictions[0][1]
        top_confidence = predictions[0][2] * 100

        # Store result
        results.append(
            (
                file,
                image,
                predictions,
                top_label,
                top_confidence
            )
        )

        # Print results in terminal
        print("=" * 55)
        print("Image:", file)
        print("=" * 55)

        for _, label, confidence in predictions:

            print(
                f"{label}: "
                f"{confidence * 100:.2f}%"
            )

        print()


    # ========================================================
    # CREATE RESULT WINDOW
    # ========================================================

    fig, axes = plt.subplots(
        2,
        3,
        figsize=(15, 10)
    )


    # Convert axes into a simple list
    axes = axes.flatten()


    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    for index, result in enumerate(results):

        file, image, predictions, top_label, top_confidence = result

        # Display image
        axes[index].imshow(image)

        # Display prediction information
        axes[index].set_title(
            f"{top_label}\n"
            f"Confidence: {top_confidence:.2f}%",
            fontsize=12
        )

        # Remove axis
        axes[index].axis("off")


    # ========================================================
    # HIDE UNUSED IMAGE BOXES
    # ========================================================

    for index in range(
        len(results),
        len(axes)
    ):

        axes[index].axis("off")


    # ========================================================
    # MAIN TITLE
    # ========================================================

    fig.suptitle(
        "🧠 Pretrained Image Classification",
        fontsize=20,
        fontweight="bold"
    )


    # ========================================================
    # ADJUST LAYOUT
    # ========================================================

    plt.tight_layout(
        rect=[0, 0, 1, 0.95]
    )


    # ========================================================
    # SHOW RESULTS
    # ========================================================

    plt.show()