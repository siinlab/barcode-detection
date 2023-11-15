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

@app.post("/detection/")
async def upload(token: str = Form(...), file: UploadFile = File(...)):
    """ Upload an image and detect cars in it.

    Args:
        token: A token to authenticate the user.
        file: The image to be uploaded.
    """
    try:
        result = process_detection_request(token=token, file=file)
        return JSONResponse(content=result)
    except Exception as e:
        # Handle exceptions appropriately
        return JSONResponse(content={"error": "An error occurred during processing."}, status_code=500)
