import os
import cv2
from configs.config import CustomConfig
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json
import numpy as np
class DataTask():
    def __init__(self, camid):
        super().__init__()
        self.camid = camid
        self.CFG = CustomConfig().CFG
        self.camcfg = self.CFG[camid][camid]
        self.camera_url = self.camcfg.get('camera_url','').strip('')
        self.frame = None
        self.input_width = int(self.camcfg.get('input_width',1280))
        self.input_height = int(self.camcfg.get('input_height', 720))




        self.frame_idx = 0
        self.ret = False
        self.frame = None

        self.read_stream()

    
    def read_stream(self):
        self.stream = cv2.VideoCapture(self.camera_url)
    
    def read_frame(self):
        ret, frame = self.stream.read()
        if not ret:
            frame = None
        else:
            frame = cv2.resize(frame, (self.input_width, self.input_height))
        self.frame_idx +=1
        return ret, frame
