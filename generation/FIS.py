from typing import Optional, Union, Tuple, List, Callable, Dict
import numpy as np
import abc
import utils
from tqdm.notebook import tqdm
import torch
from diffusers import StableDiffusionPipeline, DDIMScheduler
import torch.nn.functional as nnf
# import seq_aligner
import shutil
from torch.optim.adam import Adam
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from transformers import pipeline, set_seed
import random
import re
import sys
import cv2
current_path = os.getcwd()
print(current_path)
# sys.path.append(os.path.join(current_path, 'mask'))

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from mask.bg_removal import bg_removal

def text2img_func(pipe_text2img, prompt, figure_size):
    print(figure_size)
    # prompt = "top view of a single pumpkin, close up"
    # prompt = "A single blueberry, round, sweet fruit with a blue-black skin and juicy flesh that is high in antioxidants."
    # prompt = "A single bluberry, close up"
    # images = pipe_img2img(prompt=prompt, image=init_image, strength=0.75, guidance_scale=7.5).images
    image_text2img = pipe_text2img(prompt=prompt, width=figure_size[0], height=figure_size[1], guidance_scale=7.5).images[0]
    num = random.randint(0, 100)
    image_text2img.save("D:/speak/generation/output/"+prompt+str(num)+".png")
    return image_text2img

def image_grid(imgs, rows, cols):
    # imgs is a list containing several PIL objects
    assert len(imgs) == rows * cols

    w, h = imgs[0].size
    grid = PIL.Image.new('RGB', size=(cols * w, rows * h))
    grid_w, grid_h = grid.size

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid

def load_image(path):
    return PIL.Image.open(path).convert("1")

def get_locate(img):
    img_array = np.array(img)
    imgray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 0, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_on_img = cv2.drawContours(img_array, contours, -1, (0,255,0), 3, lineType = cv2.LINE_AA)
    contour_on_img = Image.fromarray(contour_on_img.astype(np.uint8))
    # find the largest contour(filling) and get its mask
    contours = sorted(contours, key=cv2.contourArea)   
    cntr = contours[-1] 
    return cntr

def get_attetnion_crop(bar_image,image_text2img):
    img_blend = Image.blend(bar_image,image_text2img, 0.6)
    cntr = get_locate(bar_image)
    x,y,w,h = cv2.boundingRect(cntr)
    img_blend = img_blend.crop((x,y,x+w,y+h))
    img_blend # 只有bar的那一部分
    ### 放在黑底背景上
    im_bg = Image.new("RGB", (512, 512),color="black")
    # resize the object to maintain the detail
    # resize to 512 if we need generate
    im_bg.paste(img_blend, (int(512/2-w/2), int(512/2-h/2)))
    return im_bg

def draw_circle(ratio):
    w, h = 512, 512
    shape = [(30, 30), (w - 30, h - 30)]
    # creating new Image object
    img = Image.new("RGB", (w, h))
    # create pieslice image
    img1 = ImageDraw.Draw(img)  
    img1.pieslice(shape, start = 0, end = int(360*ratio), fill ="white", outline ="white")
    return img

def img2img_func(pipe_img2img, prompt, im_bg, num_images,s =0.5):
    generator = torch.Generator(device="cuda").manual_seed(random.randint(0,99999999)) 
    n_propmt = "blurry, watermark, text, signature, frame, cg render, lights"
    output = pipe_img2img(prompt = prompt, image=im_bg, strength=s, guidance_scale=7.5, 
                        generator=generator, num_images_per_prompt=num_images, return_dict=True)
    # images.insert(0, init_image)
    images = output.images
    nfsw_checker = output.nsfw_content_detected
    images_img2img = [images[i] for i in range(len(nfsw_checker)) if not nfsw_checker[i]]
    # images_r = image_grid(images_img2img, 1, len(images_img2img))
    return images_img2img

def depth2img_func(pipe_depth, prompt, im_bg, num_images,s=0.5):
    generator = torch.Generator(device="cuda").manual_seed(random.randint(0,99999999)) 
    n_propmt = "blurry, watermark, text, signature, frame, cg render, lights"
    output = pipe_depth(prompt = prompt, negative_prompt=n_propmt, image=im_bg, strength=s, guidance_scale=7.5, generator=generator, num_images_per_prompt=num_images)
    images_depth = output.images
    return images_depth

def img_bg_removal(images):
    images_rm = []
    for i in range(len(images)):
        image = bg_removal(images[i], current_path)
        images_rm.append(image)
    return images_rm

# 得考虑是第一次生成还是再次生成
def FIS_bar(prompt, bar_mask, num_to_generate, figure_size, pipe_text2img, pipe_img2img, pipe_depth):
    if num_to_generate==4:
        images_depth2img = depth2img_func(pipe_depth, prompt, bar_mask, num_images=4)
        img_bg_depth2img = img_bg_removal(images_depth2img)
        return img_bg_depth2img
        # # step1 text2img
        # img_text2img = text2img_func(pipe_text2img, prompt, (512, 512))
        # # step2 blend(text2img+bar_mask)
        # random_number = random.uniform(0.6, 0.8)
        # img_blend = Image.blend(bar_mask,img_text2img, random_number)
        # cntr = get_locate(bar_mask)
        # x,y,w,h = cv2.boundingRect(cntr)
        # img_blend = img_blend.crop((x,y,x+w,y+h))
        # img_blend # 只有bar的那一部分
        # ### 放在黑底背景上 不然分辨率太低了
        # im_bg = Image.new("RGB", (512, 512),color="black")
        # im_bg.paste(img_blend, (int(512/2-w/2), int(512/2-h/2)))
        # # step3 img2img & depth2img
        # images_img2img = img2img_func(pipe_img2img, prompt, im_bg, num_images=2)
        # images_depth2img = depth2img_func(pipe_depth, prompt, im_bg, num_images=2)
        # # step4 bg removal
        # img_bg_img2img = img_bg_removal(images_img2img)
        # img_bg_depth2img = img_bg_removal(images_depth2img)
        # return img_bg_img2img+img_bg_depth2img
    if num_to_generate!=4:
        images_depth2img = depth2img_func(pipe_depth, prompt, bar_mask, num_images=num_to_generate)
        img_bg_depth2img = img_bg_removal(images_depth2img)
        return img_bg_depth2img

        # step1 text2img
        # img_text2img = text2img_func(pipe_text2img, prompt, figure_size)
        # # step2 blend(text2img+bar_mask)
        # random_number = random.uniform(0.6, 0.8)
        # img_blend = Image.blend(bar_mask,img_text2img, random_number)
        # cntr = get_locate(bar_mask)
        # x,y,w,h = cv2.boundingRect(cntr)
        # img_blend = img_blend.crop((x,y,x+w,y+h))
        # img_blend # 只有bar的那一部分
        # ### 放在黑底背景上 不然分辨率太低了
        # im_bg = Image.new("RGB", (512, 512),color="black")
        # im_bg.paste(img_blend, (int(512/2-w/2), int(512/2-h/2)))
        # # step3 img2img & depth2img
        # random_number = random.random()
        # if random_number > 0.5:
        #     images_img2img = img2img_func(pipe_img2img, prompt, im_bg, num_images=num_to_generate)
        #     img_bg_img2img = img_bg_removal(images_img2img)
        #     return img_bg_img2img
        # else:
        #     images_depth2img = depth2img_func(pipe_depth, prompt, im_bg, num_images=num_to_generate)
        #     img_bg_depth2img = img_bg_removal(images_depth2img)
        #     return img_bg_depth2img
        
def FIS_line(prompt, line_mask, num_to_generate, figure_size, pipe_text2img, pipe_img2img, pipe_depth):
    if num_to_generate==4:
        # step1 text2img
        img_text2img = text2img_func(pipe_text2img, prompt, figure_size)
        # step2 blend(text2img+line_mask) crop
        image_array = np.array(img_text2img)
        mask_array = np.array(line_mask)
        # mask_array = np.tile(mask_array[:,:,np.newaxis], [1,1,3])
        result_array = np.where(mask_array == 0, 0, image_array)
        img_blend = Image.fromarray(result_array)
        # step3 img2img & depth2img
        images_img2img = img2img_func(pipe_img2img, prompt, img_blend, num_images=2)
        images_depth2img = depth2img_func(pipe_depth, prompt, img_blend, num_images=2)
        # step4 bg removal
        img_bg_img2img = img_bg_removal(images_img2img)
        img_bg_depth2img = img_bg_removal(images_depth2img)
        return img_bg_img2img+img_bg_depth2img
    if num_to_generate!=4:
        # step1 text2img
        img_text2img = text2img_func(pipe_text2img, prompt, figure_size)
        # step2 blend(text2img+line_mask) crop
        image_array = np.array(img_text2img)
        mask_array = np.array(line_mask)
        # mask_array = np.tile(mask_array[:,:,np.newaxis], [1,1,3])
        result_array = np.where(mask_array == 0, 0, image_array)
        img_blend = Image.fromarray(result_array)
        random_number = random.random()
        if random_number > 0.5:
            images_img2img = img2img_func(pipe_img2img, prompt, img_blend, num_images=num_to_generate)
            img_bg_img2img = img_bg_removal(images_img2img)
            return img_bg_img2img
        else:
            images_depth2img = depth2img_func(pipe_depth, prompt, img_blend, num_images=num_to_generate)
            img_bg_depth2img = img_bg_removal(images_depth2img)
            return img_bg_depth2img

def FIS_pie(prompt, ratio, num_to_generate, figure_size, pipe_text2img, pipe_img2img, pipe_depth):
    if num_to_generate==4:
        # step1 text2img
        img_text2img = text2img_func(pipe_text2img, prompt, figure_size)
        # step2 blend(text2img+line_mask) crop
        pie_mask_circle = draw_circle(ratio=1)
        image_array = np.array(img_text2img)
        mask_array = np.array(pie_mask_circle)
        result_array = np.where(mask_array == 0, 0, image_array)
        img_blend = Image.fromarray(result_array)
        # step3 img2img & depth2img
        images_img2img = img2img_func(pipe_img2img, prompt, img_blend, num_images=2)
        images_depth2img = depth2img_func(pipe_depth, prompt, img_blend, num_images=2)
        # step4 bg removal
        img_list = images_img2img + images_depth2img
        img_new_list = []
        for img in img_list:
            image_array = np.array(img)
            mask_array = np.array(draw_circle(ratio))
            # mask_array = np.tile(mask_array[:,:,np.newaxis], [1,1,3])
            result_array = np.where(mask_array == 0, 0, image_array)
            img_blend = Image.fromarray(result_array)
            img_new_list.append(img_blend)
        return img_new_list
    if num_to_generate!=4:
        # step1 text2img
        img_text2img = text2img_func(pipe_text2img, prompt, figure_size)
        # step2 blend(text2img+line_mask) crop
        pie_mask_circle = draw_circle(ratio=1)
        image_array = np.array(img_text2img)
        mask_array = np.array(pie_mask_circle)
        result_array = np.where(mask_array == 0, 0, image_array)
        img_blend = Image.fromarray(result_array)
        random_number = random.random()
        if random_number > 0.5:
            images_img2img = img2img_func(pipe_img2img, prompt, img_blend, num_images=num_to_generate)
            img_list = images_img2img
            img_new_list = []
            mask_array = np.array(draw_circle(ratio))
            for img in img_list:
                image_array = np.array(img)
                result_array = np.where(mask_array == 0, 0, image_array)
                img_blend = Image.fromarray(result_array)
                img_new_list.append(img_blend)
            return img_new_list
        else:
            images_depth2img = depth2img_func(pipe_depth, prompt, img_blend, num_images=num_to_generate)
            img_list = images_depth2img
            img_new_list = []
            mask_array = np.array(draw_circle(ratio))
            for img in img_list:
                image_array = np.array(img)
                result_array = np.where(mask_array == 0, 0, image_array)
                img_blend = Image.fromarray(result_array)
                img_new_list.append(img_blend)
            return img_new_list


    
