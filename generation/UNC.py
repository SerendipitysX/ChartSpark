from PIL import Image
import cv2
import os
import sys
import numpy as np
import torch
import random
current_path = os.getcwd()
print(current_path)
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from mask.bg_removal import bg_removal

def text2img(pipe_text2img, prompt, figure_size, num_images):
    prompts = [prompt] * num_images
    image_text2img = pipe_text2img(prompt=prompts, width=figure_size[0], height=figure_size[1], guidance_scale=7.5).images
    return image_text2img


def crop_element_from_RGBA(image):
    img_removal = np.array(image)
    imgray = cv2.cvtColor(img_removal, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 30, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 1:
        left, top, right, bottom = image.width, image.height, 0, 0 
        for x in range(image.width): 
            for y in range(image.height): 
                if image.getpixel((x, y))[3] != 0: 
                    left = min(left, x) 
                    top = min(top, y) 
                    right = max(right, x) 
                    bottom = max(bottom, y) 
        image = image.crop((left, top, right, bottom))
    else:
        area_highest = 0
        for cntr in contours:
            x,y,w,h = cv2.boundingRect(cntr)
            if w*h > area_highest:   # find the biggest area 
                x_gen, y_gen, w_gen, h_total = x,y,w,h
                area_highest = w*h
        img_removal_correct = img_removal[y_gen:y_gen+h_total,x_gen:x_gen+w_gen]
        image = Image.fromarray(img_removal_correct).convert("RGBA")
    return image


def extract_element(image_pil, text_prompt=None, model=None, predictor=None):
    img_RGBA = bg_removal(image_pil, current_path)
    element = crop_element_from_RGBA(img_RGBA)
    return element # RGBA
