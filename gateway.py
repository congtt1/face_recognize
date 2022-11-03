from libs.extract.arcface_module import ArcFace
from libs.extract.transform import process_image
from flask import Blueprint, Flask, make_response, request, jsonify
from libs.detect.yolo_grpc_client import YoloGrpcClient
import numpy as np
import requests
import json
from subprocess import Popen
from util import dataio
import time
import os
from configs.config import CustomConfig
CFG = CustomConfig().CFG
camcfg = CFG['COMMON']['COMMON']
local_host_ip = camcfg.get('local_host_ip','192.168.1.196')

face = Blueprint('face', __name__)

time.sleep(2)
detector = YoloGrpcClient('localhost', 50100)
extractor = ArcFace('libs/extract/arcface-r100.engine')

@face.route('pattern', methods=['POST'])
def api_register_pattern():
    # data = request.get_json()
    # print(data)
    # images = data['images']
    images = request.get_json()

    encodings = []
    face_images = []

    for image in images:
        # convert bytes to array
        image = dataio.convert_bytes_to_numpy_array(image)
        # get face location and face encoding
        # face_locations = detector.detect([image])[0]
        face_locations, probs, classes = detector.predict(image)
        # validate
        if len(face_locations) != 1:
            continue
        res = face_locations[0]
        left, top, right, bottom = res
        face = image[top:bottom, left:right]
        face = process_image(face)
        face_encoding = extractor.extract(face)[0]

        # append result
        encodings.append(face_encoding)
        face_image = image[top:bottom, left:right]
        face_images.append(dataio.convert_numpy_array_to_bytes(face_image))

    if not len(encodings):
        return make_response(jsonify({
            "message": "Invalid images",
        }), 400)

    return make_response(jsonify({
        "face_images": face_images,
        "encodings": encodings,
        "message": "Success",
    }), 200)

@face.route('detect', methods=['POST'])
def detect_face():
    data = request.get_json()
    image = data["image"]
    image = dataio.convert_bytes_to_numpy_array(image)
    results = detector.detect([image])
    response = {"result":results}
    # response = {}
    response = make_response(jsonify(response),200)

    return response






@face.route('pattern', methods=['PUT'])
def api_verify_pattern():
    data = request.get_json()
    image = data["image"]

    payload = []
    # for image in images:
        # convert byte to numpy array
    unknown_image = dataio.convert_bytes_to_numpy_array(image)
    unknown_image = process_image(unknown_image)
    # get features face
    face_encodings = extractor.extract(unknown_image)[0]
    # face_encodings = [features.tolist() for features in face_encodings if type(features) == np.ndarray]
    d = {"face_images": [
            ],
            "gate_location": np.arange(len(face_encodings)).tolist(), #fake data
            "status": [1] * len(face_encodings), #fake data
            "encodings": [face_encodings]
    }
    payload.append(d)

    # POST request
    url = f"https://{local_host_ip}:8999/api/user/pattern" #https
    r = requests.put(url=url, json=payload, verify=False)
    response = make_response(jsonify(json.loads(r.text)), r.status_code)
    return response


if __name__ == '__main__':

    app = Flask(__name__)
    app.register_blueprint(face, url_prefix='/api/user')
    app.run(host="0.0.0.0", port="8501", debug=True)
