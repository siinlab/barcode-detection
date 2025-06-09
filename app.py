import streamlit as st
from PIL import Image
import numpy as np
from src.utils import load_yolo_model, draw_bounding_boxes, decode_barcodes

# Title of the app
st.title("YOLO Barcode Detection and Decoding App")

# Model selection
model_choice = st.selectbox("Select Model Type", ("Detector Model", "End-to-End Model"))

# Load YOLO models
barcode_detector_model = load_yolo_model("detector model")
barcode_decoder_model = load_yolo_model("decoder model")

# File uploader for images
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True, width=200)

    st.write("Running barcode detection...")

    # Convert the image to numpy array for drawing
    image_np = np.array(image)

    # Run YOLO barcode detection model on the uploaded image
    detection_results = barcode_detector_model(image_np)

    # Draw the bounding boxes on the image
    image_np_with_boxes = draw_bounding_boxes(detection_results, image_np)
    st.image(image_np_with_boxes, caption="Detected Barcode", use_column_width=True, width=200)

    if model_choice == "End-to-End Model":
        st.write("Running barcode number decoding...")
        
        # Decode the detected barcodes
        detected_barcodes = decode_barcodes(detection_results, image_np, barcode_decoder_model)

        # Display all detected barcodes
        if detected_barcodes:
            for i, digits in enumerate(detected_barcodes, 1):
                st.write(f"Product {i}: Detected Digits: {digits}")
        else:
            st.write("No barcodes detected.")
    else:  # Detector Model case
        st.write("Barcode detection is performed.")
