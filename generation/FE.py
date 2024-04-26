from typing import Optional, Union, Tuple, List, Callable, Dict
import numpy as np
import abc
# import utils
from tqdm.notebook import tqdm
import torch
from diffusers import StableDiffusionPipeline, DDIMScheduler
import torch.nn.functional as nnf
# import seq_aligner
import shutil
from torch.optim.adam import Adam
from PIL import Image
## FE
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import matplotlib.pyplot as plt
from transformers import pipeline, set_seed
import random
import re
import sys
import cv2
current_path = os.getcwd()
# print(current_path)
# sys.path.append(os.path.join(current_path, 'mask'))

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from mask.bg_removal import bg_removal

def text2img_element(pipe_text2img, prompt):
    image_text2img = pipe_text2img(prompt=prompt, width=512, height=512, guidance_scale=7.5).images[0]
    num = random.randint(0, 100)
    image_text2img.save("C:/Users/user/A-project/speak/generation/output/"+prompt+str(num)+".png")
    return image_text2img

def extract_element(image_text2img):
    image = bg_removal(image_text2img, current_path)
    # get mask
    image_arr = np.array(image)
    mask = image_arr[:,:,-1]
    mask = Image.fromarray(mask) 
    im_bg = Image.new("RGBA", (512, 512))
    blend_img = Image.composite(image, im_bg, mask)
    blend_img
    # get contour
    img_array = np.array(blend_img)
    imgray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 0, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_on_img = cv2.drawContours(img_array, contours, -1, (0,255,0), 3, lineType = cv2.LINE_AA)
    contour_on_img = Image.fromarray(contour_on_img.astype(np.uint8))
    # find the largest contour(filling) and get its mask
    contours = sorted(contours, key=cv2.contourArea)   
    cntr = contours[-1]  
    # print(cntr)       
    out_mask = np.zeros_like(img_array)
    mask =cv2.drawContours(out_mask, [cntr], -1, 255, cv2.FILLED)[:,:,0]
    mask = Image.fromarray(mask.astype(np.uint8)) 
    # get object with the largest contour
    blend_img = Image.composite(image, im_bg, mask)
    return blend_img
