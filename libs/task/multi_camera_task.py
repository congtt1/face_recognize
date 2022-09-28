import numpy as np
import cv2
from libs.task.check_area import InstrusionTask
from libs.task.read_data import DataTask
class SingleCameraTask():
    def __init__(self,camid):
        super(SingleCameraTask,self).__init__()
        self.camid = camid
        self.is_running = True
    def start(self):
        self.data_task = DataTask(self.camid)
        self.instrusion_task = InstrusionTask(self.camid)

    def run(self):
        while self.is_running:
            ret, frame = self.data_task.read_frame() 
            self.is_running = ret
