import torch
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image



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
            color = (0, 255, 0)  # Green for barcode
            thickness = 1  # Set the thickness of the rectangle

            # Draw bounding box and label with increased thickness
            cv2.rectangle(image_np, (x1, y1), (x2, y2), color, thickness)  # Draw rectangle
            label = f"{class_name}: {confidence:.2f}"
            cv2.putText(image_np, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    return image_np

def crop_bounding_box(image_np: np.ndarray, bounding_box) -> np.ndarray:
    """Crop the image around the bounding box."""
    x1, y1, x2, y2 = map(int, bounding_box.xyxy[0].tolist())
    cropped_image = image_np[y1:y2, x1:x2]
    return cropped_image
