import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# Define the URL of the image on Google Drive
image_url = "https://drive.google.com/uc?id=IMAGE_ID"

# Download the image
image_path = "image.jpg"
os.system(f"wget -O {image_path} {image_url}")

# Load and preprocess the image
img = image.load_img(image_path, color_mode="grayscale", target_size=(28, 28))
img_array = image.img_to_array(img)
img_array = img_array / 255.0  # Normalize the pixel values

# Expand dimensions to match the input shape expected by the model
img_array = np.expand_dims(img_array, axis=0)

# Load the trained model
model_path = "mnist_model.h5"
model = load_model(model_path)

# Make predictions
predictions = model.predict(img_array)

# Get the predicted number
predicted_number = np.argmax(predictions)

# Display the predicted number
print("Predicted Number:", predicted_number)
