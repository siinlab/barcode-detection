# Barcode Reader API

## Introduction
Welcome to the Barcode Reader API documentation. Our advanced Barcode Reader software streamlines data entry, enhances accuracy, and saves valuable time by automating the simultaneous scanning of multiple barcodes.

## Getting Started
To seamlessly integrate this powerful tool into your applications or systems, you only need a framework capable of interacting with a REST API. Whether you prefer Python, JavaScript, Java, or tools like NodeRed, the Barcode Reader API effortlessly fits into your workflow.

> Note: In this guide, we'll be providing examples using **Python**.

To access the software, an API Key is mandatory to authorization. Obtain your key from the [Platform](https://platform.siinlab.com/active_products).   

Once you have your API Key, the following Python code demonstrates how to use the Barcode Reader API on this image:

<img src="https://siin.b-cdn.net/images/barcode.jpeg" height="300px">

```python
from os import getenv
from PIL import Image
import requests
import json
image_url = 'https://i.ibb.co/jg4KQhN/1.jpg'
api_url = "http://ai.siinlab.com/barcode/v1/detection/"
image_path = 'image.png'
api_key = getenv('SIIN_API_KEY')
assert api_key, 'Please set the API Key'

image = Image.open(requests.get(image_url, stream=True).raw)
image.save(image_path)

files = {'file': ('image.jpg', open(image_path, 'rb').read())}
payload = {"token": api_key}

response = requests.post(url=api_url, files=files, data=payload)
if response.status_code != 200:
    print('Error')

with open('image.png', 'wb') as f:
    f.write(response.content)
```

The API response will return the foreground in a png format file:
```
[
   {
      "x1": 154.5421600341797,
      "y1": 448.8489990234375,
      "x2": 754.0051879882812,
      "y2": 692.7383422851562,
      "score": 0.9243909120559692,
      "barcode": "4607023704821"
   }
]
```
## Endpoints
The API exposes two endpoints:

- GET `/status` - Check Status:
By accessing this endpoint, users can check the status of the server. The server's status message is returned in a JSON format with a 200 status.

- POST `/v1/detection/` - Upload for detection:
This endpoint is dedicated to uploading images for barcode scanning. The request is formatted as multipart/form-data, and successful detections return JSON response. Validation errors are communicated with a 422 status.

- GET `/v1/detection/` - Python example:
This endpoint now provides a Python example illustrating the proper utilization of the POST `/v1/detection/` endpoint.

- POST `/v2/detection/` - Upload for detection:
This endpoint replicates the functionality of the V1 version outlined previously, albeit with a revised input format. It mandates the input image to be presented as a byte array.

- GET `/v2/detection/` - Python example:
This endpoint now provides a Python example illustrating the proper utilization of the POST `/v2/detection/` endpoint.

Feel free to explore the functionality of both endpoints to integrate barcode scanning seamlessly into your applications and systems.

## API version
{{api-version}}

## ChangeLog
{{change-log}}
