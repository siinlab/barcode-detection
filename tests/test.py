import os
import shutil
from utils.evaluation import evaluate_model

# Configuration file for paths
import os

__here__ = os.path.dirname(os.path.abspath(__file__))

IMAGES_FOLDER = os.path.join(__here__, "test dataset", "images")
LABELS_FOLDER = os.path.join(__here__, "test dataset", "labels")
MISRECOGNIZED_FOLDER = os.path.join(__here__, "misrecognized")

def main():
    """model evaluation."""
    images_folder = IMAGES_FOLDER
    labels_folder = LABELS_FOLDER
    misrecognized_folder = MISRECOGNIZED_FOLDER
    
    # remove misrecognized folder if it exists
    if os.path.exists(misrecognized_folder):
        shutil.rmtree(misrecognized_folder)
        
    # create misrecognized folder
    os.makedirs(misrecognized_folder)

    accuracy = evaluate_model(images_folder, labels_folder, misrecognized_folder)
    print(f"Model accuracy: {accuracy} %")

if __name__ == "__main__":
    main()
