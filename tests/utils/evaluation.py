import os
import cv2
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

    for image_name in os.listdir(images_folder):
        image_path = os.path.join(images_folder, image_name)
        label_path = os.path.join(labels_folder, os.path.splitext(image_name)[0] + '.txt')

        if os.path.isfile(image_path) and os.path.isfile(label_path):
            actual_barcodes = read_labels(label_path)
            ground_truths.append(bool(actual_barcodes))
            api_response = run_inference(image_path)

            if api_response:
                detected_barcodes, img = process_detections(api_response, image_path)
            else:
                detected_barcodes = []

            is_match = set(detected_barcodes) == set(actual_barcodes)
            if not is_match:
                save_misrecognized_image(img, misrecognized_folder, image_name)
            predictions.append(is_match)
        print("detected_barcodes",detected_barcodes, "actual_barcodes",actual_barcodes)
        print("ground_truths",ground_truths, "detected_barcodes",predictions)

    return accuracy_score(ground_truths, predictions) * 100
