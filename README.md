# Barcode Detection and Recognition System.

##### This project is designed for Barcode Detection and Recognition. It leverages YOLO models for detecting barcodes, a decoder for recognizing barcode information, and integrates with Streamlit for a user-friendly web interface
---
## 🎥 Video Demo
https://github.com/user-attachments/assets/008efa1a-a3ff-4f7e-b8d0-92da2650014d

## 📑 Project Structure

```bash
BARCODE-DETECTION/
│
├── data/
│   ├── barcode_detection_data/   # Training data for barcode detection
│   │   ├── images/               # Contains images used for training/testing
│   │   ├── labels/               # Contains corresponding labels for the images
│   │   ├── data.yaml             # Data configuration file
│   │   ├── test.txt              # Test dataset paths
│   │   ├── train.txt             # Training dataset paths
│   │   └── val.txt               # Validation dataset paths
│   └── barcode_recognition_data/ # Data used for barcode recognition
│   │   ├── images/               # Contains images used for training/testing
│   │   ├── labels/               # Contains corresponding labels for the images
│   │   ├── data.yaml             # Data configuration file
│   │   ├── test.txt              # Test dataset paths
│   │   ├── train.txt             # Training dataset paths
│   │   └── val.txt               # Validation dataset paths
│
├── models/                       
│   ├── barcode_decoder/          # Model for barcode recognition (decoder)
│   │   └── decoder_model.pt      # Trained model for decoding barcode data
│   ├── barcode_detector/         # Models for barcode detection
│   │   ├── detector_model1.pt    # Barcode detection model 1
│   │   └── detector_model2.pt    # Barcode detection model 2
│
├── src/                          # Source code for core functions and utilities
│   ├── inference.py              # Code for inference and model predictions
│   ├── train.py                  # Code for training the models
│   └── utils.py                  # Utility functions
│
├── .gitignore                    # Files and directories to ignore in Git
├── Dockerfile                    # Docker configuration file
├── app.py                        # Streamlit app for the barcode detection and recognition system
├── README.md                     # Project documentation (this file)
└── requirements.txt              # Python dependencies

```
## 🚀 How to Run the Application

### 1. Clone the Repository
Open a terminal and run the following command:

```bash
git clone  https://github.com/siinlab/barcode-detection.git
cd BARCODE-DETECTION
```
### 2. Install Dependencies
Make sure you have `Python 3.9+` installed. Install the required dependencies:

```bash
pip install -r requirements.txt
```
### 3. Run the Application
Use the following command to run the Streamlit application:

```bash
streamlit run app.py
```
Open your browser and go to:

```bash
http://localhost:8501
```
## 🐳 Using Docker
### 1. Build the Docker Image
Ensure Docker is installed and running on your system. Build the Docker image with:

```bash
docker build -t barcode-app .
```
### 2. Run the Docker Container
Run the container and expose the app on port 8501:

```bash
docker run -p 8501:8501 barcode-app
```
### 3. Access the Application
Open your browser and navigate to:

```bash
http://localhost:8501
```
## 📋 Features
- **Barcode Detection**: Detects barcodes in uploaded images.
- **Barcode Recognition**: Recognizes and decodes the barcode information from detected barcodes.
- **End-to-End Flow**: Processes an image to detect barcodes and decode the information.

## 🛠️ Training Models

To train the barcode detection and recognition models, the training datasets should be prepared in the `data/training_data` directory. For more details on how to prepare the datasets, refer to the [README](data/training_data/README.md).

### 1. Training Barcode Detection Model

To train the detection model, you can use the `train.py` script. Run the following commands:

```bash
cd data/training_data/barcode-detection/
python ../../../src/train.py --data ./data.yaml --model ../../../models/barcode-detection/model.yaml --epochs 30 --batch 8 --imgsz 640
```

### 2. Training Barcode Recognition Model

You can train the recognition model using the `train.py` script, by running the following commands:

```bash
cd data/training_data/barcode-recognition/
python ../../../src/train.py --data ./data.yaml --model ../../../models/barcode-recognition/model.yaml --epochs 120 --batch 8 --imgsz 128
```

## 📄 License
This project is licensed under the MIT License.

## ✨ Contributing
- Fork the repository.
- Create a new branch (git checkout -b feature-branch).
- Make your changes and commit them (git commit -m 'Add feature').
- Push the branch (git push origin feature-branch).
- Open a Pull Request.

## 📞 Contact
If you have any questions or issues, feel free to open a Github issue or reach out at [contact@siinlab.com](mailto:contact@siinlab.com).
