from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import List

from fastapi.responses import HTMLResponse

from yolo_utils import process_detection_request
from config import BarcodeOutput, Status

from engine_utils import load_api_keys, api_key_router, ApiKeyException, html_documentation
from engine_utils.requests import api_key_is_valid
from engine_utils.dependencies import validate_api_key, get_pil_image

from engine_utils.pydantic_models import Image, ApiKey, Status
from engine_utils.dependencies import validate_api_key, get_pil_image

from os.path import join, abspath, dirname

from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix='/v2')


@router.post("/detection/", response_model=List[BarcodeOutput])
async def upload(api_key: ApiKey = Depends(validate_api_key), image: Image = Depends(get_pil_image)):
    """ Formatted as (x1, y1, x2, y2, score, barcode string)
    """
    try:
        result = process_detection_request(None, image=image)
        return result
    except Exception as e:
        # Handle exceptions appropriately
        raise HTTPException(detail="An error occurred during processing.", status_code=500)
    
@router.get('/detection/', response_class=PlainTextResponse)
async def v2_example():
    return """
from os import getenv
from PIL import Image
import numpy as np
import requests

image_url = 'https://i.ibb.co/jg4KQhN/1.jpg'
api_url = "https://ai.siinlab.com/barcode/v2/detection/"
image_path = 'image.png'
api_key = getenv('SIIN_API_KEY') # export SIIN_API_KEY=xxxxx
assert api_key, 'Please set the API Key'

headers = {'x-api-key': api_key}

# Prepare input data
image = Image.open(requests.get(image_url, stream=True).raw).convert('RGB')
array = np.array(image).astype('uint8')
height, width, channels = array.shape
payload = {'image': array.tobytes().decode('latin1'), 'height': height, 'width': width, 'channels': channels}

response = requests.post(url=api_url, json=payload, headers=headers)
if response.status_code != 200:
    print(response.text)
    print('Error')
    exit(1)
    
# Read response
print(response.json())
"""