import os
import shutil
from utils.evaluation import evaluate_model
import config

def main():
    """model evaluation."""
    images_folder = config.IMAGES_FOLDER
    labels_folder = config.LABELS_FOLDER
    misrecognized_folder = config.MISRECOGNIZED_FOLDER
    
    # remove misrecognized folder if it exists
    if os.path.exists(misrecognized_folder):
        shutil.rmtree(misrecognized_folder)
        
    # create misrecognized folder
    os.makedirs(misrecognized_folder)

    accuracy = evaluate_model(images_folder, labels_folder, misrecognized_folder)
    print(f"Model accuracy: {accuracy} %")

if __name__ == "__main__":
    main()
