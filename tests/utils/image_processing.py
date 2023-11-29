import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import requests
import os
from supervision.detection.core import Detections
from supervision.detection.annotate import BoxAnnotator

# Initialize box annotator for image processing
box_annotator = BoxAnnotator(thickness=3, text_thickness=3, text_scale=2)

def run_inference(image_file):
    """Run model inference on a given image."""
    if not image_file:
        return None

    image = Image.open(image_file)
    image_bytes = convert_image_to_bytes(image)
    return send_request(image_bytes)

def convert_image_to_bytes(image):
    """Convert PIL image to bytes."""
    image_bytes = BytesIO()
    image.save(image_bytes, format=image.format)
    return image_bytes.getvalue()

def send_request(image_bytes):
    """Send a request to a detection API with an image."""
    url = "http://localhost:9002/detection/"
    files = {'file': ('image.jpg', image_bytes)}
    payload = {"token": "1234"}

    response = requests.post(url=url, files=files, data=payload)
    if response.status_code != 200:
        return None
    return response.json()

def process_detections(img, class_id, labels, xyxy, confidence):
    
    """Process detections from the API response."""
   
    # Converting to numpy arrays
    xyxy = np.array(xyxy)
    confidence = np.array(confidence)
    class_id = np.array(class_id)

    # Creating a Detections object
    detections = Detections(xyxy=xyxy, confidence=confidence, class_id=class_id)
   
    # Annotating the image
    img = box_annotator.annotate(scene=img, detections=detections, labels=labels)
    return img

def save_misrecognized_image(image, folder, image_name):
    """Save misrecognized images to a specified folder."""
    cv2.imwrite(os.path.join(folder, image_name), image)
