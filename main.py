import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from PIL import Image


# Load the pretrained MobileNetV2 model
model = tf.keras.applications.MobileNetV2(weights="imagenet")


# Folder containing our sample images
IMAGE_FOLDER = "sample_images"


# Function to classify an image
def classify_image(image_path):

    # Open the image
    image = Image.open(image_path).convert("RGB")

    # Resize image to 224 x 224
    image = image.resize((224, 224))

    # Convert image to NumPy array
    image_array = np.array(image)

    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)

    # Preprocess the image
    image_array = tf.keras.applications.mobilenet_v2.preprocess_input(
        image_array
    )

    # Make prediction
    predictions = model.predict(image_array, verbose=0)

    # Get top 3 predictions
    decoded_predictions = (
        tf.keras.applications.mobilenet_v2.decode_predictions(
            predictions, top=3
        )[0]
    )

    return image, decoded_predictions


# Find images in the sample_images folder
image_files = [
    file for file in os.listdir(IMAGE_FOLDER)
    if file.lower().endswith((".jpg", ".jpeg", ".png"))
]


# Check if images are available
if not image_files:

    print("No images found in the sample_images folder.")

else:

    # Classify each image
    for file in image_files:

        image_path = os.path.join(IMAGE_FOLDER, file)

        image, predictions = classify_image(image_path)

        print("\n" + "=" * 50)
        print("Image:", file)
        print("=" * 50)

        # Display predictions
        for _, label, confidence in predictions:
            print(f"{label}: {confidence * 100:.2f}%")

        # Get the top prediction
        top_label = predictions[0][1]
        top_confidence = predictions[0][2] * 100

        # Display image
        plt.figure(figsize=(6, 5))
        plt.imshow(image)
        plt.title(
            f"Prediction: {top_label}\n"
            f"Confidence: {top_confidence:.2f}%"
        )
        plt.axis("off")
        plt.show()