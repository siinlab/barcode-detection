import argparse
from ultralytics import YOLO
import torch

def parse_args():
    parser = argparse.ArgumentParser(description="Train YOLOv8 on custom dataset")
    parser.add_argument('--data', type=str, default='data.yaml', help='dataset YAML path')
    parser.add_argument('--model', type=str, default='yolov8n.pt', help='pretrained model or custom .pt')
    parser.add_argument('--epochs', type=int, default=50, help='number of epochs')
    parser.add_argument('--batch', type=int, default=16, help='batch size')
    parser.add_argument('--imgsz', type=int, default=640, help='image size (px)')
    return parser.parse_args()

def main():
    args = parse_args()
    model = YOLO(args.model)
    model.train(
        data=args.data,
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        device='cuda' if torch.cuda.is_available() else 'cpu',
        # augmentation options:
        degrees=90,  # random rotation degrees [-180, 180]
        flipud=0.3,  # random up-down flip
        fliplr=0.3,  # random left-right flip
        translate=0.1,  # random translation percentage
        erasing=0.0,  # random erasing probability
    )

if __name__ == '__main__':
    main()
