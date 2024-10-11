import torch
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image

def load_yolo_model(model_choice: str) -> YOLO:
    """Load the YOLO model based on user's selection."""
    if model_choice == "detector model 1":
        model_path = "models/barcode_detector/detector_model1.pt"
    elif model_choice == "detector model 2":
        model_path = "models/barcode_detector/detector_model2.pt"
    else:
        model_path = "models/barcode_decoder/decoder_model.pt"

    return YOLO(model_path)

def draw_bounding_boxes(results, image_np: np.ndarray) -> np.ndarray:
    """Draw bounding boxes on the image using YOLO detection results."""
    for result in results:
        for box in result.boxes:
            # Extract the bounding box coordinates and confidence score
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            confidence = box.conf[0].item()
            class_id = int(box.cls[0])
            class_name = result.names[class_id]
            # Define clear color and thickness for the bounding box
            color = (0, 0, 0)  # Bright yellow in BGR format
            thickness = 6  # Set the thickness of the rectangle

            # Draw bounding box and label with increased thickness
            cv2.rectangle(image_np, (x1, y1), (x2, y2), color, thickness)  # Draw rectangle
            label = f"{class_name}: {confidence:.2f}"
            cv2.putText(image_np, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    return image_np

def process_uploaded_image(uploaded_file) -> np.ndarray:
    """Convert uploaded image to a NumPy array for further processing."""
    image = Image.open(uploaded_file).convert("RGB")
    return np.array(image)

