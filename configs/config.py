import os
import glob
import configparser
class CustomConfig():
    def __init__(self):
        super(CustomConfig,self).__init__()
        self.cam_folder = 'cam_configs'
        self.camid_list = []
        self.CFG = {}
        self.parse_cam_configs()
    def parse_cam_configs(self):
        cam_keys = [os.path.join(self.cam_folder, file) for file in os.listdir(self.cam_folder) if file.endswith('.ini')]
        for cfg_path in cam_keys:
            name_file = cfg_path.split('/')[-1]
            name_file = name_file.split('.ini')[0]
            self.camid_list.append(name_file)
            config = configparser.ConfigParser()
            config.sections()
            config.read(cfg_path)
            self.CFG[name_file] = config

