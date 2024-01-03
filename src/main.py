from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import List

from yolo_utils import process_detection_request
from config import BarcodeOutput, Status

from engine_utils import load_api_keys, api_key_router, ApiKeyException, validate_api_key

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_api_keys('barcode')
        
    yield # this is where the rest of the app would go
    
    print('Shutting down ...')

app = FastAPI(lifespan=lifespan)
app.include_router(api_key_router)

@app.get("/status", response_model=Status)
async def check_status():
    """ Check the status of the server.
    Returns:
        str: A message indicating if the server is running.
    """
    return Status(status='ok')    

@app.post("/detection/", response_model=List[BarcodeOutput])
async def upload(token: str = Form(...), file: UploadFile = File(...)):
    """ Formatted as (x1, y1, x2, y2, score, barcode string)
    """
    try:
        if not validate_api_key(token):
            raise ApiKeyException("Invalid API key")
        
        result = process_detection_request(token=token, file=file)
        return result
    except ApiKeyException as e:
        raise HTTPException(detail=str(e), status_code=401)
    except Exception as e:
        # Handle exceptions appropriately
        raise HTTPException(detail="An error occurred during processing.", status_code=500)
