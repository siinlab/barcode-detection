import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import requests
import os
from supervision.detection.core import Detections
from supervision.detection.annotate import BoxAnnotator

# Initialize box annotator for image processing
box_annotator = BoxAnnotator(thickness=2, text_thickness=1, text_scale=1)

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

def process_detections(api_response, image_path):
    """Process detections from the API response."""
    img = cv2.imread(image_path)
    xyxy, confidence, detected_barcodes = zip(*[
        ([det["x1"], det["y1"], det["x2"], det["y2"]], det["score"], int(det["barcode"]) if det["barcode"] else "")
        for det in api_response
    ])

    # Converting to numpy arrays
    xyxy = np.array(xyxy)
    confidence = np.array(confidence)
    class_id = np.array(detected_barcodes)

    # Creating a Detections object
    detections = Detections(xyxy=xyxy, confidence=confidence, class_id=class_id)

    # Generating labels
    labels = [f"{id} {conf:0.2f}" for conf, id in zip(confidence, class_id)]

    # Annotating the image
    img = box_annotator.annotate(scene=img, detections=detections, labels=labels)
    return detected_barcodes, img

def save_misrecognized_image(image, folder, image_name):
    """Save misrecognized images to a specified folder."""
    cv2.imwrite(os.path.join(folder, image_name + ".jpg"), image)
