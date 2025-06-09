import torch
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
from lgg import logger

logger.setLevel("DEBUG")

def load_yolo_model(model_choice: str) -> YOLO:
    """Load the YOLO model based on user's selection."""
    if model_choice == "detector model":
        model_path = "models/barcode-detection/model.pt"
    else:
        model_path = "models/barcode-recognition/model.pt"

    return YOLO(model_path)

def draw_bounding_boxes(results, image_np: np.ndarray) -> np.ndarray:
    """Draw bounding boxes on the image using YOLO detection results."""
    image_np = image_np.copy()  # Create a copy to avoid modifying the original image
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            confidence = box.conf[0].item()
            class_id = int(box.cls[0])

            color = (0, 255, 0)  # Green for barcode
            # Set thickness based on box width (min 1, max 4)
            box_width = x2 - x1
            thickness = max(1, min(4, box_width // 100))
            cv2.rectangle(image_np, (x1, y1), (x2, y2), color, thickness)
            # label = f"{class_id}: {confidence:.2f}"
            label = f"{class_id}"
            # Set font thickness based on box width (min 1, max 3)
            font_thickness = max(1, min(3, box_width // 150))
            # Set font scale based on box height (min 0.3, max 1.0)
            font_scale = max(0.4, min(1.0, box_width / 200 if box_width > box_width else box_width / 200))
            cv2.putText(image_np, label, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 100, 255), font_thickness)

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

            # Add 10% padding to each side
            pad_w = int(bounding_box[2] * 0.1)
            pad_h = int(bounding_box[3] * 0.1)
            x1 = int(bounding_box[0] - bounding_box[2] // 2 - pad_w)
            y1 = int(bounding_box[1] - bounding_box[3] // 2 - pad_h)
            x2 = int(bounding_box[0] + bounding_box[2] // 2 + pad_w)
            y2 = int(bounding_box[1] + bounding_box[3] // 2 + pad_h)
            # Ensure coordinates are within image bounds
            x1 = max(x1, 0)
            y1 = max(y1, 0)
            x2 = min(x2, image_np.shape[1])
            y2 = min(y2, image_np.shape[0])
            # Crop the barcode region from the image
            cropped_barcode = image_np[y1:y2, x1:x2]

            # save cropped barcode for debugging
            cropped_barcode_pil = Image.fromarray(cropped_barcode)
            cropped_barcode_pil.save("debug_cropped_barcode.png")

            # Run the decoder model on the cropped barcode
            decoding_results = barcode_decoder_model(cropped_barcode, nms=True, conf=0.5, iou=0.2)
            
            # Save the cropped barcode image with detections for debugging
            debug_cropped_barcode_with_detections = draw_bounding_boxes(decoding_results, cropped_barcode)
            debug_cropped_barcode_with_detections = Image.fromarray(debug_cropped_barcode_with_detections)
            debug_cropped_barcode_with_detections.save("debug_cropped_barcode_with_detections.png")
            
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
