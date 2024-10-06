# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install necessary packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and models
COPY src/app.py ./src/app.py
COPY src/utils.py ./src/utils.py
COPY src/inference.py ./src/inference.py
COPY src/train.py ./src/train.py
COPY models/barcode_detector/ ./models/barcode_detector/
COPY models/barcode_decoder/ ./models/barcode_decoder/
COPY data/ ./data/
COPY src/output_images/ ./src/output_images/

# Expose the port for Streamlit
EXPOSE 8501

# Set the command to run the Streamlit application
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
