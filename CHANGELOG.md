
### 0.2.0
- Introducing a novel inference endpoint, `/v2/detection/`, facilitating the submission of input images as byte arrays within a JSON object that includes additional fields: `height`, `width`, and `channels`.
- The `/v1/detection/` is still usable.
- Implemented a GET method for each detection endpoint, specifically GET /v1/detection/ and GET /v2/detection/. These endpoints now provide Python examples demonstrating the proper utilization of the API through each respective inference endpoint.

### 0.1.0
- Implementation of the first version of barcode reader.
- The API can be consumed via a POST request to the `/v1/detection/` endpoint by sending the input image as a file (`.jpg`, `.png`, etc.).