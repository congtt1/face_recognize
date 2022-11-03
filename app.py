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
    out_fps = 6
    sleep_time = 1 / out_fps
    endpoint_api = 'http://0.0.0.0:8501/api/user/pattern'
    start_time = time.time()    
    # start_time 
    encoding = "utf-8"
    number_frame = 0
    while(is_runing):
        # for camid in list_cam:
        with open(f'{camid}.csv','a') as write:
            writer = csv.writer(write)
            ret, frame = data_task.read_frame()
            start = time.time()
            num_frame +=1
            fps = round(num_frame / (time.time() - start_time),2)
            # print(fps, num_frame, camid, end='\r')
            if fps < out_fps:
                continue
            boxs, scores, _ = detector.predict(frame)
            # print(boxs)
            for box in boxs:
                instrusions = instrusion_task.check_insutrion(box)
                if sum(instrusions) > 0:
                    xmin, ymin, xmax, ymax = box
                    image = frame[ymin:ymax, xmin:xmax]
                    image = dataio.convert_numpy_array_to_bytes(image)
                    data = {"image":image}
                    res = requests.put(endpoint_api, json=data)
                    res = res.json()['responses']
                    res = res[0][0][0]
                    score_cosine = res['score']
                    mail = res['zcfg_requester_address_email']
                    if score_cosine > score_cosine_theshold:
                        if camid == 'cam02':
                            door_id = 3
                        else:
                            for i, j in enumerate(instrusions):
                                if j:
                                    door_id = str(i)
                        Popen(["python3", "open_door.py", "--door_id", door_id], stdin=PIPE, encoding=encoding)
                    writer.writerow([num_frame, score_cosine, mail, xmin, ymin, xmax,ymax])
            time.sleep(max(0, sleep_time - time.time() + start))
