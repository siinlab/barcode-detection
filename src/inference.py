import argparse
import cv2
import numpy as np
from PIL import Image
from utils import load_yolo_model, draw_bounding_boxes, process_uploaded_image

def main(image_path: str, model_choice: str):
    # Load YOLO model
    model = load_yolo_model(model_choice)

    # Open and process the image
    image = Image.open(image_path).convert("RGB")
    image_np = np.array(image)

    # Run YOLO model on the image
    print(f"Running {model_choice} model on {image_path}...")
    results = model(image_np)

    # Draw bounding boxes on the image
    image_np = draw_bounding_boxes(results, image_np)

    # Save or display the output image
    output_image_path = "src/output_images/output_detected_image.jpg"
    cv2.imwrite(output_image_path, cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
    print(f"Results saved to {output_image_path}")



if __name__ == "__main__":
    # Set up argument parsing for command-line interface
    parser = argparse.ArgumentParser(description="Run YOLO barcode detection on an image.")
    parser.add_argument("image_path", type=str, help="Path to the image file.")
    parser.add_argument("model_choice", type=str, choices=["detector model 1", "detector model 2", "decoder model"],
                        help="Choose a model for barcode detection.")
    
    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args.image_path, args.model_choice)
