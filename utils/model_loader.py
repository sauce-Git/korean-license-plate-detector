# This code is for loading model from local directory

import os

from ultralytics import YOLO

DEFAULT_MODEL_PATH = './content/ultralytics/trained/'
DEFAULT_WEIGHTS_PATH = '/weights/best.pt'


def set_model_path(model_name): # This function is for absolute path of model
    model_path = DEFAULT_MODEL_PATH + model_name + DEFAULT_WEIGHTS_PATH
    return model_path


def load_model(model_name): # This function is for loading model
    model_path = set_model_path(model_name)
    model = YOLO(model_path)
    return model
