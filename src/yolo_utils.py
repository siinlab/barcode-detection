import traceback
from datetime import datetime
from os.path import join
from os.path import split, splitext
from typing import List
from typing import Tuple, Union

import PIL
import numpy as np
from fastapi import File, UploadFile, Form, HTTPException
from lgg import logger
from ultralytics import YOLO

from config import BARCODE_PATH, BARCODE_DECODER_PATH
from utils import is_valid_token, save_uploaded_image

def validate_token(token: str):
    if not is_valid_token(token):
        logger.error(f"Token `{token}` is invalid")
        raise HTTPException(status_code=498, detail="Invalid token")

def handle_json_response(bboxes: List[np.array], label_names: List[dict]):
    logger.debug(f"Returning json response")
    js_response = {
        "bboxes": [b.tolist() for b in bboxes],
        "labelNames": label_names
    }
    logger.debug(f'js_response: {js_response}')
    return js_response

def process_detection_request(token: str = Form(...),
                              file: UploadFile = File(...)):
    """ Process a detection request. """

    logger.info(f"Detecting in {file.filename}...")

    validate_token(token)

    try:
        path = save_uploaded_image(file)
        logger.info(f"Successfully uploaded {file.filename}")

        bboxes, label_names = detect_barcode(input_source=path)
        
        return handle_json_response(bboxes, label_names)
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"There was an error uploading the file: {tb}")
        raise HTTPException(status_code=500, detail="There was an error running inference on the image")
    finally:
        file.file.close()


def detect_barcode(input_source: Union[str, PIL.Image.Image]) ->\
    Tuple[PIL.Image.Image, Tuple[List[np.ndarray], List[dict]]]:
    """ Detect barcodes in an image.

    Args:
        input_source: The source of the image to detect barcodes. Can be a path to an image or a PIL.Image object.

    Returns:
        - bboxes: A list of np.array containing the bounding boxes of detected barcodes.
        - labels: A list of dictionaries containing details of the detected barcodes.
    """
    return predict(BARCODE_PATH, input_source)

def detect_barcode_digits(input_source: Union[str, PIL.Image.Image]) ->\
    Tuple[PIL.Image.Image, Tuple[List[np.ndarray], List[dict]]]:
    """
    Detect barcode_digits in an image.

    Args:
        input_source: The source of the image to detect barcodes. Can be a path to an image or a PIL.Image object.

    Returns:
        - bboxes: A list of np.array containing the bounding boxes of detected barcodes.
        - labels: A list of dictionaries containing details of the detected barcodes.
    """
    return predict(BARCODE_DECODER_PATH, input_source)

def predict(model_path: str, input_source: Union[str, PIL.Image.Image]) -> \
        Tuple[PIL.Image.Image, Tuple[List[np.ndarray], List[dict]]]:
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