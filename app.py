import streamlit as st
from PIL import Image
import numpy as np
import cv2
from ultralytics import YOLO
from src.utils import load_yolo_model, draw_bounding_boxes

# Title of the app
st.title("YOLO Barcode Detection App")

# Model selection
model_choice = st.selectbox("Choose a model:", 
                            ["detector model 1", "detector model 2", "decoder model "])

# Load the selected YOLO model using the function from utils.py
model = load_yolo_model(model_choice)

# File uploader for images
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Run the model if an image is uploaded
if uploaded_file is not None:
    # Open the image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    st.write("Running detection...")

    # Convert the image to numpy array for drawing
    image_np = np.array(image)

    # Run YOLO model on the uploaded image
    results = model(image_np)

    # Draw the bounding boxes on the image using the function from utils.py
    image_np = draw_bounding_boxes(results, image_np)

    # Show the results image with boxes
    st.image(image_np, caption="Detected Objects", use_column_width=True)
