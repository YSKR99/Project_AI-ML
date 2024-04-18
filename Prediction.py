import os
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import tensorflow as tf

# Function to fetch the latest image from Google Drive folder
def fetch_latest_image(folder_url):
    # Assuming the folder URL is in the format you provided
    # Fetch the list of files in the folder
    response = requests.get(folder_url)
    # Extract image URLs from the response HTML content
    image_urls = [line.split('"')[1] for line in response.text.split('\n') if 'data-id' in line and 'href="/file/' in line]
    # Get the URL of the latest image
    latest_image_url = image_urls[-1]
    return latest_image_url

# Function to download image from URL
def download_image(image_url, destination_path):
    # Download the image
    response = requests.get(image_url)
    image_data = response.content
    # Write the image data to a file
    with open(destination_path, 'wb') as f:
        f.write(image_data)

# Function to preprocess image and predict number
def predict_number(image_path, model):
    img = Image.open(image_path).convert('L')  # Convert image to grayscale
    img = img.resize((28, 28))  # Resize image to MNIST input size
    img_array = np.expand_dims(np.array(img), axis=0) / 255.0  # Normalize pixel values
    prediction = np.argmax(model.predict(img_array), axis=-1)
    return prediction[0]

# Example usage
def main():
    # Load the pre-trained MNIST model
    model = tf.keras.models.load_model('mnist_model.h5')  # Update with your model path
    
    # Google Drive folder URL
    folder_url = 'https://drive.google.com/drive/folders/1XRfdSIle1WPrcmXS5kwbycN7tdIHJPlE/'
    
    # Fetch the URL of the latest image
    latest_image_url = fetch_latest_image(folder_url)
    
    # Path to save the downloaded image
    destination_path = 'downloaded_image.jpg'
    
    # Download the latest image
    download_image(latest_image_url, destination_path)
    
    # Predict the number
    predicted_number = predict_number(destination_path, model)
    print('Predicted number:', predicted_number)

if __name__ == "__main__":
    main()