import os
from enum import Enum
from os.path import dirname, join

from PIL import Image
from lgg import logger
import cv2
import requests
import numpy as np
from config import API_KEY_URL

UPLOAD_FOLDER = join(dirname(__file__), "uploads")
RESULT_FOLDER = join(dirname(__file__), "results")
DEBUG_FOLDER = join(dirname(__file__), "debug")


def is_valid_token(token: str) -> bool:
    """ Check if the token is valid.
    Args:
        token (str): A token to validate.
    Returns:
        bool: True if the token is valid, False otherwise.
    """
    return True

def save_uploaded_image(file) -> str:
    """ Save the uploaded file inside `uploads` folder.

    Note:
        - `uploads` folder is created if it doesn't exist.

    Args:
        file (UploadFile): The uploaded file.

    Returns:
        str: The path to the saved file.
    """
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    
    path = join(UPLOAD_FOLDER, file.filename)
    
    # Read the image from the uploaded file
    image_data = file.file.read()
    # Convert image data to numpy array
    nparr = np.frombuffer(image_data, np.uint8)

    # Decode the image using OpenCV
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    cv2.imwrite(path, image)

    return image


def save_result_image(img_name: str, img: Image.Image) -> str:
    """ Save the uploaded file inside `results` folder.

    Note:
        - `results` folder is created if it doesn't exist.

    Args:
        img_name (str): The name of the image.
        img (PIL.Image): The image with the bounding boxes.

    Returns:
        str: The path to the saved image.
    """
    os.makedirs(RESULT_FOLDER, exist_ok=True)

    path = join(RESULT_FOLDER, img_name)
    img.save(path)

    return path

def save_debug_image(img_name: str, img: Image.Image) -> str:
    """ Save the uploaded file inside `debug` folder.

    Note:
        - `debug` folder is created if it doesn't exist.

    Args:
        img_name (str): The name of the image.
        img (PIL.Image): The image with the bounding boxes.

    Returns:
        str: The path to the saved image.
    """
    os.makedirs(DEBUG_FOLDER, exist_ok=True)

    path = join(DEBUG_FOLDER, img_name)
    img.save(path)

    return path


def get_src_path() -> str:
    """ Get the path to the src folder.

    Returns:
        str: The path to the src folder.
    """
    return dirname(__file__)

def json_post_request(url, **kwargs):
    """ Make a post request.

    Args:
        url (str): The url to make the request to.
        **kwargs: The arguments to pass to the request.

    Returns:
        dict: The response from the request.
    """
    logger.info(f"Making a post request to {url}: {kwargs}...")
    kwargs = '&'.join([f'{k}={v}' for k, v in kwargs.items()])
    url = f'{url}?{kwargs}'
    x = requests.post(url)
    return x.json()

def crop_object( xyxy, image):
        """
        Crop the object based on its bounding box coordinates.

        Args:
            xyxy (tuple): Bounding box coordinates.
            image (np.array): The image from which to crop.

        Returns:
            np.array: The cropped object.
        """
        xmin, ymin, xmax, ymax = map(int, xyxy[:4])
        width, height = xmax - xmin, ymax - ymin
        width_increase, height_increase = int(0.4 * width), int(0.8 * height)

        xmin, ymin = max(0, xmin - width_increase // 2), max(0, ymin - height_increase // 2)
        xmax, ymax = min(image.shape[1], xmax + width_increase // 2), min(image.shape[0], ymax + height_increase // 2)

        return image[ymin:ymax, xmin:xmax]