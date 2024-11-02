import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO
from src.utils import load_yolo_model, draw_bounding_boxes, crop_bounding_box

# Title of the app
st.title("YOLO Barcode Detection and Decoding App")

# Model selection
model_choice = st.selectbox("Select Model Type", ("Detector Model", "End-to-End Model"))

# Load YOLO models
barcode_detector_model = load_yolo_model("detector model 1")
barcode_decoder_model = load_yolo_model("decoder model ")

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

        detected_barcodes = []  # Store results for all barcodes

        # Iterate through all detected bounding boxes
        for result in detection_results:
            for box in result.boxes:
                # Crop each barcode area
                cropped_barcode = crop_bounding_box(image_np, box)

                # Run the decoder model on the cropped barcode
                decoding_results = barcode_decoder_model(cropped_barcode)

                # Collect digits and their x1 coordinates for sorting
                detected_info = [
                    (int(digit_box.cls[0]), digit_box.xyxy[0][0].item())
                    for digit_result in decoding_results
                    for digit_box in digit_result.boxes
                ]

                # Sort digits by their x1 coordinate (left-to-right order)
                detected_info.sort(key=lambda x: x[1])

                # Form the final detected digits string
                detected_digits = ''.join(str(digit[0]) for digit in detected_info)

                # Save the decoded barcode
                if detected_digits:
                    detected_barcodes.append(detected_digits)
                else:
                    detected_barcodes.append("No digits detected.")

        # Display all detected barcodes
        if detected_barcodes:
            for i, digits in enumerate(detected_barcodes, 1):
                st.write(f"Product {i}: Detected Digits: {digits}")
        else:
            st.write("No barcodes detected.")

    else:  # Detector Model case
        st.write("Barcode detection is performed.")
