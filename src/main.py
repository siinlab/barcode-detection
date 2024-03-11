from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import List

from fastapi.responses import HTMLResponse

from yolo_utils import process_detection_request
from config import BarcodeOutput, Status

from engine_utils import load_api_keys, api_key_router, ApiKeyException, html_documentation
from engine_utils.requests import api_key_is_valid
from engine_utils.dependencies import validate_api_key, get_pil_image


from os.path import join, abspath, dirname

from contextlib import asynccontextmanager


from v1 import router as v1_router
from v2 import router as v2_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_api_keys('barcode')
        
    yield # this is where the rest of the app would go
    
    print('Shutting down ...')

app = FastAPI(lifespan=lifespan)
app.include_router(api_key_router)
app.include_router(v1_router)
app.include_router(v2_router)

@app.get('/')
async def get_documentation():
    path = join(abspath(dirname(__file__)), '..')
    html = html_documentation(join(path, 'Documentation.md'),
                              join(path, 'VERSION'),
                              join(path, 'CHANGELOG.md'))
    return HTMLResponse(content=html)

@app.get("/status", response_model=Status)
async def check_status():
    """ Check the status of the server.
    Returns:
        str: A message indicating if the server is running.
    """
    return Status(status='ok')

