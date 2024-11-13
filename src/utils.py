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

            color = (0, 255, 0)  # Green for barcode
            thickness = 1
            cv2.rectangle(image_np, (x1, y1), (x2, y2), color, thickness)
            label = f"Class {class_id}: {confidence:.2f}"
            cv2.putText(image_np, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    return image_np

def rotate_image_if_needed(image_np, bounding_box):
    """Rotate the image if the barcode is detected in an unusual orientation."""
    x1, y1, x2, y2 = map(int, bounding_box[:4])
    width = x2 - x1
    height = y2 - y1

    # Rotate 90 degrees if width < height (barcode is vertical)
    if width < height:
        image_np = cv2.rotate(image_np, cv2.ROTATE_90_CLOCKWISE)
    # Rotate 180 degrees if the barcode might be upside down
    elif y2 < y1:
        image_np = cv2.rotate(image_np, cv2.ROTATE_180)

    return image_np

def convert_xyxy_to_xywh(box):
    """Convert bounding box from (xmin, ymin, xmax, ymax) to (center_x, center_y, width, height, confidence, class_id).
    
    Args:
        box: Bounding box in either an object format (with xyxy attribute) or list format [xmin, ymin, xmax, ymax, confidence, class_id].

    Returns:
        list: Converted bounding box in (center_x, center_y, width, height, confidence, class_id) format.
    """
    # Check if box is a list or tuple with expected length
    if isinstance(box, (list, tuple)) and len(box) >= 6:
        xmin, ymin, xmax, ymax, confidence, class_id = box
    # Otherwise, assume it's an object with attributes like xyxy, conf, and cls
    elif hasattr(box, 'xyxy') and hasattr(box, 'conf') and hasattr(box, 'cls'):
        xmin, ymin, xmax, ymax = map(int, box.xyxy[0].tolist())
        confidence = box.conf[0].item()
        class_id = int(box.cls[0])
    else:
        raise ValueError("Unexpected box format: box must be a list with coordinates or an object with xyxy attribute")

    width, height = xmax - xmin, ymax - ymin
    center_x, center_y = xmin + width // 2, ymin + height // 2
    return [center_x, center_y, width, height, confidence, class_id]


def sort_barcode_digits(barcode_digits, barcode_box):
    """ Sort the barcode digits in the correct order.

    Args:
        barcode_digits (list): List of detected barcode digit bounding boxes.
        barcode_box (list): Bounding box of the barcode.

    Returns:
        list: Sorted barcode digits.
    """
    # Convert barcode box to center format
    barcode_box = convert_xyxy_to_xywh(barcode_box)
    converted_digits = [convert_xyxy_to_xywh(digit) for digit in barcode_digits]
    
    # Extract center coordinates
    digits_cx = np.array([digit[0] for digit in converted_digits])
    digits_cy = np.array([digit[1] for digit in converted_digits])
    
    barcode_width, barcode_height = barcode_box[2], barcode_box[3]
    
    # Determine orientation based on standard deviation
    if np.std(digits_cx) > np.std(digits_cy):
        # Barcode is horizontal
        sorted_indices = digits_cx.argsort()
        if digits_cy.mean() < (barcode_height * 1.2) / 2:
            sorted_indices = sorted_indices[::-1]  # Reverse if upside down
    else:
        # Barcode is vertical
        sorted_indices = digits_cy.argsort()
        if digits_cx.mean() > (barcode_width * 1.2) / 2:
            sorted_indices = sorted_indices[::-1]  # Reverse if upside down
        
    sorted_digits = [int(converted_digits[i][5]) for i in sorted_indices]
    return sorted_digits

def decode_barcodes(detection_results, image_np, barcode_decoder_model):
    """Decode detected barcodes and return a list of detected digits."""
    detected_barcodes = []

    # Iterate through all detected bounding boxes
    for result in detection_results:
        for box in result.boxes:
            bounding_box = convert_xyxy_to_xywh(box)
            
            # Rotate the image if needed
            image_np = rotate_image_if_needed(image_np, bounding_box)

            # Crop each barcode area
            x1, y1, x2, y2 = int(bounding_box[0] - bounding_box[2] // 2), int(bounding_box[1] - bounding_box[3] // 2), int(bounding_box[0] + bounding_box[2] // 2), int(bounding_box[1] + bounding_box[3] // 2)
            cropped_barcode = image_np[y1:y2, x1:x2]

            # Run the decoder model on the cropped barcode
            decoding_results = barcode_decoder_model(cropped_barcode)

            # Collect detected digits as bounding boxes
            detected_info = [
                [int(digit_box.xyxy[0][0].item()), int(digit_box.xyxy[0][1].item()), int(digit_box.xyxy[0][2].item()), int(digit_box.xyxy[0][3].item()), 
                 digit_box.conf[0].item(), int(digit_box.cls[0])]
                for digit_result in decoding_results
                for digit_box in digit_result.boxes
            ]

            # Sort and collect digits
            sorted_digits = sort_barcode_digits(detected_info, bounding_box)
            detected_digits = ''.join(str(digit) for digit in sorted_digits)

            if detected_digits:
                detected_barcodes.append(detected_digits)
            else:
                detected_barcodes.append("No digits detected.")

    return detected_barcodes
