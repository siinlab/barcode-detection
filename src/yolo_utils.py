import traceback
from typing import List, Tuple, Union

from io import BytesIO
import PIL
import numpy as np
from fastapi import File, UploadFile, Form, HTTPException
from lgg import logger
from ultralytics import YOLO
import cv2

from config import BARCODE_PATH, BARCODE_DECODER_PATH, BarcodeOutput
from utils import save_uploaded_image
from engine_utils import validate_api_key

def validate_token(token: str):
    if not validate_api_key(token):
        logger.error(f"Token `{token}` is invalid")
        raise HTTPException(status_code=498, detail="Invalid token")

def handle_json_response(bboxes: List[np.array], label_names: List[str]) -> dict:
    """Process bounding boxes and label names to create a JSON response."""
    barcode_outputs = []

    for bbox, label_name in zip(bboxes, label_names):
        x1, y1, x2, y2, score, _ = bbox
        barcode_output = BarcodeOutput(
            x1=float(x1), y1=float(y1), x2=float(x2), y2=float(y2),
            score=float(score), barcode=label_name
        )
        barcode_outputs.append(barcode_output)

    output_list = [
        [barcode_output.x1, barcode_output.y1, barcode_output.x2, barcode_output.y2,
         barcode_output.score, barcode_output.barcode] for barcode_output in barcode_outputs
    ]

    result = {"output": output_list}
    return result

def process_detection_request(token: str = Form(...), file: UploadFile = File(...)):
    """Process a detection request."""
    logger.info(f"Detecting in {file.filename}...")

    validate_token(token)

    try:
        image = save_uploaded_image(file)
        logger.info(f"Successfully uploaded {file.filename}")

        bboxes, _ = detect_barcode(input_source=image)
        label_digits, barcode_bboxes = [], []

        for xyxy in bboxes[0]:
            barcode_bboxes.append(xyxy)
            cropped_object = crop_object(xyxy, image)
            bboxe, _ = detect_barcode_digits(cropped_object)

            bboxe = bboxe[0]
            sorted_bbox_array = bboxe[bboxe[:, 0].argsort()]
            sorted_c_values = map(int, sorted_bbox_array[:, 5])
            label_digits.append(''.join(map(str, sorted_c_values)))

        return handle_json_response(barcode_bboxes, label_digits)
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"There was an error uploading the file: {tb}")
        raise HTTPException(status_code=500, detail="There was an error running inference on the image")
    finally:
        file.file.close()

def detect_barcode(input_source: Union[str, PIL.Image.Image]) -> Tuple[PIL.Image.Image, Tuple[List[np.ndarray], List[dict]]]:
    """ Detect barcodes in an image.

    Args:
        input_source: The source of the image to detect barcodes. Can be a path to an image or a PIL.Image object.

    Returns:
        - bboxes: A list of np.array containing the bounding boxes of detected barcodes.
        - labels: A list of dictionaries containing details of the detected barcodes.
    """
    return predict(BARCODE_PATH, input_source)

def detect_barcode_digits(input_source: Union[str, PIL.Image.Image]) -> Tuple[PIL.Image.Image, Tuple[List[np.ndarray], List[dict]]]:
    """
    Detect barcode_digits in an image.

    Args:
        input_source: The source of the image to detect barcodes. Can be a path to an image or a PIL.Image object.

    Returns:
        - bboxes: A list of np.array containing the bounding boxes of detected barcodes.
        - labels: A list of dictionaries containing details of the detected barcodes.
    """
    return predict(BARCODE_DECODER_PATH, input_source)

def predict(model_path: str, input_source: Union[str, PIL.Image.Image]) -> Tuple[PIL.Image.Image, Tuple[List[np.ndarray], List[dict]]]:
    """ Predict the bounding boxes in an image.

    Args:
        model_path: Path to the trained model
        input_source: The source of the image to make predictions on. Can be a path to an image or a PIL.Image object.

    Returns:
        + img: A PIL.Image object containing the image with the bounding boxes
        + (bboxes, label_names): A tuple containing the bounding boxes and the label names
    """
    bboxes, label_names = predict_bbox(model_path, input_source)
    logger.debug(f"{bboxes=}")
    logger.debug(f"{label_names=}")

    return bboxes, label_names

def predict_bbox(model_path: str, input_source: Union[str, PIL.Image.Image]) -> Tuple[List[np.ndarray], List[dict]]:
    """ Predict the bounding boxes in an image.

    Args:
        model_path: Path to the trained model
        input_source: The source of the image to make predictions on. Can be a path to an image or a PIL.Image object.

    Returns:
        - bboxes: A list of np.array containing the xyxysc bounding boxes (N, 6) per image
        - labels: A list of dictionary containing the labels names (N, C) per image
    """
    model = YOLO(model_path)
    results = model(input_source)
    bboxes = [result.boxes.data.cpu().numpy() for result in results]
    labels = [result.names for result in results]
    return bboxes, labels
