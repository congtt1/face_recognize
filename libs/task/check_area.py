import cv2
import numpy as np
from configs.config import CustomConfig
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json
class InstrusionTask():
    def __init__(self, camid):
        super().__init__()
        self.camid = camid
        self.CFG = CustomConfig().CFG
        self.camcfg = self.CFG[camid][camid]

        self.body_ratio = int(self.camcfg.get('body_ratio',5))
        self.min_height_box = int(self.camcfg.get('min_height_box',85))
        self.max_height_box = int(self.camcfg.get('max_height_box', 150))
        self.areas = self.camcfg.get('areas',[])
        self.input_width = int(self.camcfg.get('input_width',1280))
        self.input_height = int(self.camcfg.get('input_height', 720))
        self.activate_areas = {}
        self.polygons = {}
        self.x_areas = {}
        self.load_areas()

    def load_areas(self):
        self.areas = json.loads(self.areas)
        for i, area in enumerate(self.areas):
            area = np.array(area)
            area = np.reshape(area, (-1,2))
            self.activate_areas[i] = area

            self.polygons[i] = Polygon(area)
            minx = min(area[:,0])
            maxx = max(area[:,1])
            self.x_areas[i] = [minx, maxx]
    def check_insutrion(self, face_box):
        xmin, ymin, xmax ,ymax = face_box
        w = xmax - xmin
        h = ymax - ymin

        cx = int(xmin + w/2)
        cy = int(ymin + h/2)

        point_x = cx
        point_y = cy + int(cy * self.body_ratio)
        point_check = np.array([point_x, point_y])

        instrutions = []
        for key in self.polygons:
            x_limit = self.x_areas[key]
            in_area = False
            area = self.polygons[key]
            if (area.contains(Point(point_check)) or (point_x >= x_limit[0] and point_x <= x_limit[1] and point_y >= self.input_height)) and (h >= self.min_height_box and h <= self.max_height_box):
                in_area = True
            instrutions.append(in_area)
        return instrutions
