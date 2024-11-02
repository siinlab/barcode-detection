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
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            confidence = box.conf[0].item()
            class_id = int(box.cls[0])
            class_name = result.names[class_id]
            color = (0, 255, 0)  # Green for barcode
            thickness = 1

            cv2.rectangle(image_np, (x1, y1), (x2, y2), color, thickness)
            label = f"{class_name}: {confidence:.2f}"
            cv2.putText(image_np, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    return image_np

def crop_bounding_box(image_np: np.ndarray, bounding_box) -> np.ndarray:
    """Crop the image around the bounding box."""
    x1, y1, x2, y2 = map(int, bounding_box.xyxy[0].tolist())
    cropped_image = image_np[y1:y2, x1:x2]
    return cropped_image

def determine_barcode_orientation(barcode_digits, barcode_box):
    """
    Sort barcode digits based on the orientation of the barcode.
    
    Args:
        barcode_digits (list): List of detected barcode digit information.
        barcode_box (object): Bounding box object containing coordinates.

    Returns:
        list: Sorted list of barcode digits.
    """
    # Extract coordinates of bounding box
    x1, y1, x2, y2 = map(int, barcode_box.xyxy[0].tolist())
    width = x2 - x1
    height = y2 - y1

    # Determine if the barcode is horizontal or vertical
    if width > height:
        # Sort digits from left-to-right (horizontal orientation)
        sorted_digits = sorted(barcode_digits, key=lambda x: x[1])
    else:
        # Sort digits from top-to-bottom (vertical orientation)
        sorted_digits = sorted(barcode_digits, key=lambda x: x[2])

    return sorted_digits

def decode_barcodes(detection_results, image_np, barcode_decoder_model):
    """Decode detected barcodes and return a list of detected digits."""
    detected_barcodes = []

    # Iterate through all detected bounding boxes
    for result in detection_results:
        for box in result.boxes:
            # Crop each barcode area
            cropped_barcode = crop_bounding_box(image_np, box)

            # Run the decoder model on the cropped barcode
            decoding_results = barcode_decoder_model(cropped_barcode)

            # Collect digits and their coordinates for sorting
            detected_info = [
                (int(digit_box.cls[0]), digit_box.xyxy[0][0].item(), digit_box.xyxy[0][1].item())
                for digit_result in decoding_results
                for digit_box in digit_result.boxes
            ]

            # Sort digits by orientation (horizontal or vertical)
            detected_info = determine_barcode_orientation(detected_info, box)

            # Form the final detected digits string
            detected_digits = ''.join(str(digit[0]) for digit in detected_info)

            # Save the decoded barcode
            if detected_digits:
                detected_barcodes.append(detected_digits)
            else:
                detected_barcodes.append("No digits detected.")

    return detected_barcodes
