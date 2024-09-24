from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import List

from fastapi.responses import HTMLResponse

from config import BarcodeOutput, Status

from contextlib import asynccontextmanager


from v1 import router as v1_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Starting up ...')
    
    yield # this is where the rest of the app would go
    
    print('Shutting down ...')

app = FastAPI(lifespan=lifespan)
app.include_router(v1_router)

@app.get("/", response_model=Status)
async def check_status():
    """ Check the status of the server.
    Returns:
        str: A message indicating if the server is running.
    """
    return Status(status='ok')

