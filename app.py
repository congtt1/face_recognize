import cv2
import numpy as np
from libs.task.read_data import DataTask
from libs.task.check_area import InstrusionTask
import csv
from subprocess import Popen
import time
from libs.detect.yolo_grpc_client import YoloGrpcClient
import requests
from util import dataio
import json
import csv
if __name__ == '__main__':

    detector = YoloGrpcClient('localhost', 50100)
    list_cam = ['cam01', 'cam02']
    data_task1 = DataTask('cam01')
    data_task2 = DataTask('cam02')

    instrusion_task1 = InstrusionTask('cam01')
    instrusion_task2 = InstrusionTask('cam02')
    is_runing = True
    data_task_list = {'cam01':data_task1, 'cam02':data_task2}
    instrusion_task_list = {'cam01':instrusion_task1, 'cam02':instrusion_task2}
    num_frame_list = {'cam01':0, 'cam02':0}
    out_fps = 10
    sleep_time = 1 / out_fps
    endpoint_api = 'http://192.168.1.11:8501/api/user/pattern'
    start_time = time.time()    
    # start_time 
    while(is_runing):
        for camid in list_cam:
            with open(f'{camid}.csv','a') as write:
                writer = csv.writer(write)
                data_task = data_task_list[camid]
                ret, frame = data_task.read_frame()
                start = time.time()
                num_frame_list[camid] +=1
                num_frame = num_frame_list[camid]
                fps = round(num_frame / (time.time() - start_time),2)
                # print(fps, num_frame, camid, end='\r')
                if fps < out_fps:
                    continue
                instrusion_task = instrusion_task_list[camid]
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
                        writer.writerow([num_frame, score_cosine, mail, xmin, ymin, xmax,ymax])
                time.sleep(max(0, sleep_time - time.time() + start))
 