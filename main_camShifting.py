import sys
import logging
import cv2, imagehash, time, datetime
from PIL import Image
import yaml
import concurrent.futures

from verify_camShifting import is_shifted_camera

nro_threads = 6
                
with open('/workspace/shiftCamera/config/app_config.yaml') as f:
    app_cfg = yaml.load(f)

logging.basicConfig(format="%(asctime)s: %(message)s", 
                        level=logging.INFO,
                        datefmt="%H:%M:%S")

def thread_function(uri, name):
    cap = cv2.VideoCapture(uri) # 20 seg
    ret, img = cap.read()
    try:
        out = is_shifted_camera(img, name)
    except Exception as e:
        print(e)
    
args = ((dic['uri'], dic['name']) for dic in app_cfg['sources'])
with concurrent.futures.ThreadPoolExecutor(max_workers=nro_threads) as executor:
    executor.map(lambda p: thread_function(*p), args)
