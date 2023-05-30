import os

from flask import Flask
from transformers import DetrFeatureExtractor, DetrForObjectDetection


UPLOAD_FOLDER = os.path.join('static', 'uploads')
RESULT_FOLDER = os.path.join('static', 'results')

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 ** 12
app.config['feature_extractor'] = DetrFeatureExtractor.from_pretrained(
    'facebook/detr-resnet-50')
app.config['model'] = DetrForObjectDetection.from_pretrained(
    'facebook/detr-resnet-50')
app.config['frames_to_process'] = 3  # 10
