import os
import cv2
from paddleocr import PPStructure, draw_structure_result, save_structure_res
from PIL import Image
from sklearn.cluster import KMeans
import numpy as np

current_path = os.path.dirname(os.getcwd())

#  paddle ocr
from paddleocr import PaddleOCR, draw_ocr

ocr = PaddleOCR(use_angle_cls=True, lang='en')  # need to run only once to download and load model into memory
img_path = current_path + '/data/barchart_83.png'
result = ocr.ocr(img_path, cls=True)
number_dict = {}
text_dict = {}
for idx in range(len(result)):
    res = result[idx]
    for line in res:  # [[[431.0, 500.0], [472.0, 504.0], [470.0, 522.0], [429.0, 518.0]], ('Year', 0.9996013045310974)]
        if line[1][0].isdigit():
            number_dict[line[1][0]] = line[0]
        else:
            text_dict[line[1][0]] = line[0]

number_arr = np.array(list(number_dict.values)).reshape(len(number_dict), -1)

x_column = number_arr[:, 0]
diff = np.diff(x_column)
K = np.where(diff > (number_arr[0, 2]-number_arr[0, 0])*0.5)[0][0]+1
print(K)

