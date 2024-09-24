import os
import numpy as np
import cv2
from tqdm import tqdm
from .image_processing import run_inference, process_detections, save_misrecognized_image

def read_labels(file_path):
    """Read and return non-empty lines from a given file."""
    with open(file_path, 'r') as file:
        return [int(line) for line in file.read().splitlines() if line]

def accuracy_score(true_labels, predicted_labels):
    """Calculate the accuracy of predictions against true labels."""
    correct_predictions = sum(truth == prediction for truth, prediction in zip(true_labels, predicted_labels))
    return correct_predictions / len(true_labels)

def evaluate_model(images_folder, labels_folder, misrecognized_folder):
    """Evaluate model accuracy on a set of images and labels."""
    predictions, ground_truths = [], []

    for image_name in tqdm(os.listdir(images_folder)):
        image_path = os.path.join(images_folder, image_name)
        label_path = os.path.join(labels_folder, os.path.splitext(image_name)[0] + '.txt')

        if os.path.isfile(image_path) and os.path.isfile(label_path):
            actual_barcodes = set(read_labels(label_path))

            api_response = run_inference(image_path)

            img = cv2.imread(image_path)
            respond = False
            if api_response:
                xyxy, confidence, detected_barcodes = zip(*[
                            ([det["x1"], det["y1"], det["x2"], det["y2"]], det["score"], int(det["barcode"]) if det["barcode"] else 0)
                            for det in api_response
                        ])
                detected_barcodes = [barcode for  barcode in detected_barcodes]
                respond = True 
            else:
                detected_barcodes  = []
                confidence = []

            is_match = set(detected_barcodes) == actual_barcodes
            label = []
            for conf, detected_barcode in zip(confidence, detected_barcodes):
                ground_truths.append(True)
                label.append("success") if detected_barcode in actual_barcodes else label.append(f"{detected_barcode}  {conf:0.2f}")
                
                predictions.append(detected_barcode in actual_barcodes)
            if respond:
                img = process_detections(img, detected_barcodes, label, xyxy, confidence)
            if not is_match:
                save_misrecognized_image(img, misrecognized_folder, image_name)

    return accuracy_score(ground_truths, predictions) * 100

