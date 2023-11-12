from fastapi.responses import JSONResponse

from fastapi import FastAPI
from fastapi import File, UploadFile, Form

from yolo_utils import process_detection_request

app = FastAPI()


@app.get("/status")
async def check_status():
    """ Check the status of the server.
    Returns:
        str: A message indicating if the server is running.
    """
    return JSONResponse({'status': 'ok'})


@app.post("/detection/")
async def upload(token: str = Form(...),
                 file: UploadFile = File(...),
                 ):
    """ Upload an image and detect cars in it.

    Args:
        token: A token to authenticate the user.
        file: The image to be uploaded.
    """
    return process_detection_request(token=token,
                                     file=file)