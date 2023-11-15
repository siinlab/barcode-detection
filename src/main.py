from fastapi import FastAPI, File, UploadFile, Form
from typing import List
from fastapi.responses import JSONResponse

from yolo_utils import process_detection_request
from config import BarcodeOutput, Status

app = FastAPI()

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
        result = process_detection_request(token=token, file=file)
        return result
    except Exception as e:
        # Handle exceptions appropriately
        return JSONResponse(content={"error": "An error occurred during processing."}, status_code=500)
