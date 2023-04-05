import os
import cv2
from paddleocr import PPStructure, draw_structure_result, save_structure_res
from PIL import Image
from sklearn.cluster import KMeans
import numpy as np

current_path = os.path.dirname(os.getcwd())

 # paddle structure
# table_engine = PPStructure(show_log=True, image_orientation=True)

# save_folder = './output'
# img_path = current_path + '/data/barchart_83.png'
# img = cv2.imread(img_path)
# result = table_engine(img)
# save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])
#
# for line in result:
#     line.pop('img')
#     print(line)
#
# font_path = 'doc/fonts/simfang.ttf'  # PaddleOCR下提供字体包
# image = Image.open(img_path).convert('RGB')
# im_show = draw_structure_result(image, result, font_path=font_path)
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')

#  paddle ocr
from paddleocr import PaddleOCR, draw_ocr
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
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

# the first is left and top || the last is right and bottom
# the problem is to find the K
x_column = number_arr[:, 0]
diff = np.diff(x_column)
K = np.where(diff > (number_arr[0, 2]-number_arr[0, 0])*0.5)[0][0]+1
print(K)

# # detector set-up
# y_detector = [1, 0, 1, 0, 1, 0, 1, 0]
# x_detector = [0, 1, 0, 1, 0, 1, 0, 1]
# a = np.mean(number_arr, axis=1)



# # draw result
# from PIL import Image
# result = result[0]
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')
