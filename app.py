import cv2
import numpy as np
from libs.task.read_data import DataTask
from libs.task.check_area import InstrusionTask
import csv
from subprocess import Popen,PIPE
import time
from libs.detect.yolo_grpc_client import YoloGrpcClient
import requests
from util import dataio
import json
import csv
import argparse
from gpio import *
from configs.config import CustomConfig
import cv2
parser = argparse.ArgumentParser()

if __name__ == '__main__':
    parser.add_argument('--camid', default="cam01", type=str, help="list camera for capture, usage: 1,2 for cam01, cam02 or 0-2 for cam00, cam01, cam02. Leave it empty for all cameras")
    args = parser.parse_args()
    init_gpio()
    camid = args.camid
    CFG = CustomConfig().CFG
    camcfg = CFG[camid][camid]
    score_cosine_theshold = camcfg.getfloat('score_cosine_theshold',0.3)

    detector = YoloGrpcClient('localhost', 50100)
    data_task = DataTask(camid)

    instrusion_task = InstrusionTask(camid)
    is_runing = True
    num_frame = 0
    last_frame = 0
    out_fps = 6
    sleep_time = 1 / out_fps
    endpoint_api = 'http://0.0.0.0:8501/api/user/pattern'
    start_time = time.time()    
    # start_time 
    encoding = "utf-8"
    number_frame = 0
    while(is_runing):
        ret, frame = data_task.read_frame()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        start = time.time()
        num_frame +=1
        fps = round(num_frame / (time.time() - start_time),2)
        if fps < out_fps:
            continue
        boxs, scores, _ = detector.predict(frame)
        for box in boxs:
            instrusions = instrusion_task.check_insutrion(box)
            if sum(instrusions) > 0:
                xmin, ymin, xmax, ymax = box
                xmin = max(0, xmin)
                ymin = max(0,ymin)
                xmax = min(frame.shape[1], xmax)
                ymax = min(frame.shape[0], ymax)
                image = frame[ymin:ymax, xmin:xmax]
                image = dataio.convert_numpy_array_to_bytes(image)
                data = {"image":image}
                if num_frame - last_frame > 5:
                    res = requests.put(endpoint_api, json=data,timeout=3)
                    last_frame = num_frame
                #try:
                    res = res.json()['responses']
                    print(res)
                    if len(res) > 0:
                        res = res[0][0]
                        score_cosine = res['score']
                        #mail = res['zcfg_requester_address_email']
                        if score_cosine > score_cosine_theshold:
                            if camid == 'cam02':
                                door_id = 3
                            else:
                                for i, j in enumerate(instrusions):
                                    if j:
                                        door_id = str(i)
                            Popen(["python3", "open_door.py", "--door_id", door_id], stdin=PIPE, encoding=encoding)
                #except:
                    #continue
        time.sleep(max(0, sleep_time - time.time() + start))
