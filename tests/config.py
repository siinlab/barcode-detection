# Configuration file for paths
import os

__here__ = os.path.dirname(os.path.abspath(__file__))

IMAGES_FOLDER = os.path.join(__here__, "test dataset", "images")
LABELS_FOLDER = os.path.join(__here__, "test dataset", "labels")
MISRECOGNIZED_FOLDER = os.path.join(__here__, "misrecognized")

