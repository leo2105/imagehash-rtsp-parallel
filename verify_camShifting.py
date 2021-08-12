import cv2, imagehash
from PIL import Image
import logging
import sys

def is_shifted_camera(img, cam_name):
    
    with open(f"/workspace/shiftCamera/config/{cam_name}.txt", "r") as f:
        values = f.read().split(',')

    if len(values) != 3:
        status, last_hash_img, th = 'None', 'None', 20
    else:
        status, last_hash_img, th = values[0], values[1], int(values[2])

    status = "None"
    try:
        curr_hashimg = imagehash.average_hash(Image.fromarray(img))
    except:
        curr_hashimg = None
        
    if not(last_hash_img == 'None' or curr_hashimg is None):
        if sys.version_info.minor >= 7:
            last_hash_img = imagehash.hex_to_hash(last_hash_img)
        else:
            last_hash_img = imagehash.old_hex_to_hash(last_hash_img)
        diff = curr_hashimg - last_hash_img
        status = "Shifted" if diff > th else "Same"

    last_hash_img = curr_hashimg
    output = f"{status},{str(last_hash_img)},{th}"
    logging.info(f"Camera {cam_name}, Output: {output}")
    
    with open(f"/workspace/shiftCamera/config/{cam_name}.txt", "w") as f:
        f.write(output)


"""
img1 = cv2.imread('..\Downloads\img1.jpeg')
img2 = cv2.imread('..\Downloads\img2.jpeg')

res = is_shifted_camera(img1,'10_150_50_90')
print(res)
res = is_shifted_camera(img2,'10_150_50_90')
print(res)
"""
