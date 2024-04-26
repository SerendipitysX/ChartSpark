from typing import Any
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImagePath
import PIL
import cv2
import sys
import numpy as np
import torch
import random
import os
import json
from scipy.optimize import minimize
# from daam import trace, set_seed
current_path = os.getcwd()
print(current_path)
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from mask.bg_removal import bg_removal
from generation.model_utils import load_model_from_config, get_attn_mask
from grid.grid_compile import *
from scipy.spatial import distance

## ==================== Load model ====================
# Paths and prompt
# device = "cuda"
# config="C:/Users/user/A-project/speak/generation/config/v1-inference.yaml"
# ckpt = "C:/Users/user/A-project/speak/generation/model/sd-v1-4-full-ema.ckpt"

# Generation parameters
# scale=3
# h=512
# w=512
# ddim_steps=45
# ddim_eta=0.0
# torch.manual_seed(0)
# # model = load_model_from_config(config, ckpt, device)

# # layer definition
# hidden_layers = {}
# hidden_layer_names = []
# default_hidden_layer_name = "model.diffusion_model.middle_block.1.transformer_blocks.0.attn2"
# hidden_layer_select = None

def is_similar(color):
    threshold = 18
    white = (255, 255, 255)
    black = (0, 0, 0)
    return distance.euclidean(color, white) <= threshold or distance.euclidean(color, black) <= threshold

def extract_colors(image):
    image_array = np.array(image)
    pixels = image_array.reshape(-1, 3)
    # Calculate color counts
    color_counts = np.unique(pixels, axis=0, return_counts=True)
    colors = color_counts[0]
    counts = color_counts[1]
    valid_indices = [i for i, color in enumerate(colors) if not is_similar(color)]

    colors = colors[valid_indices]
    counts = counts[valid_indices]

    # Find the index of the most common color
    most_common_index = np.argmax(counts)
    # Get the most common color
    most_common_color = tuple(colors[most_common_index])

    return most_common_color

def replace_black_with_color(image, color):
    width, height = image.size

    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            if r == 0 and g == 0 and b == 0:
                image.putpixel((x, y), color)
    return image

def depth2img(pipe_depth, prompt, chart_mask, num_images, s=0.5):
    generator = torch.Generator(device="cuda").manual_seed(random.randint(0,99999999)) 
    n_propmt = "blurry, watermark, text, signature, frame, cg render, lights"
    output = pipe_depth(prompt = prompt, negative_prompt=n_propmt, image=chart_mask, strength=s, guidance_scale=7.5, 
                        generator=generator, num_images_per_prompt=num_images).images
    return output

def img2img(pipe_img2img, prompt, im_bg, num_images, s=0.5):
    generator = torch.Generator(device="cuda").manual_seed(random.randint(0,99999999)) 
    output = pipe_img2img(prompt = prompt, image=im_bg, strength=s, guidance_scale=7.5, 
                        generator=generator, num_images_per_prompt=num_images, return_dict=True)
    # images.insert(0, init_image)
    images = output.images
    nfsw_checker = output.nsfw_content_detected
    images_img2img = [images[i] for i in range(len(nfsw_checker)) if not nfsw_checker[i]]
    return images_img2img

def text2img(pipe_text2img, prompt, figure_size, num_images):
    prompts = [prompt] * num_images
    image_text2img = pipe_text2img(prompt=prompts, width=figure_size[0], height=figure_size[1], guidance_scale=7.5).images
    return image_text2img

def paint2img(pipe_paint, pipe_text2img, mask_pil, nums_for_pe, prompt, init_img = None):
    generator = torch.Generator(device="cuda").manual_seed(random.randint(0,99999999))
    init_image = Image.new("RGB", mask_pil.size, "white") if init_img is None else init_img
    example_image = pipe_text2img(prompt=prompt, width=512, height=512, 
                    guidance_scale=5.5, generator=generator).images[0] if init_img is None else init_img
    output_pil_list = pipe_paint(image=init_image, mask_image=mask_pil, example_image=example_image, 
               generator=generator, num_images_per_prompt=nums_for_pe).images
    return output_pil_list

def crop_element_from_RGBA(image, mask_single_FLAG= True):
    img_removal = np.array(image)
    imgray = cv2.cvtColor(img_removal, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 30, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 1 or mask_single_FLAG == False:
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

def crop_and_blend(bg_image_pil, mask_pil, alpha_channel=None, color=None):
    image_array = np.array(bg_image_pil)
    mask_array = np.array(mask_pil)
    color_array = np.full_like(mask_array, color) if color!=None else 0
    if alpha_channel is None:
        if mask_array.ndim!=2:
            image_array = np.where(mask_array == 0, color_array, image_array) if color!=None else np.where(mask_array == 0, 255, image_array)
        else:
            image_array = np.where(np.expand_dims(mask_array, axis=2) == 0, color_array, image_array) if color!=None else np.where(mask_array == 0, 255, image_array)
    else: #add fourth-dim(alpha) for bg_image, set 0 according to mask
        image_array = np.concatenate((image_array, np.full((mask_pil.size[1], mask_pil.size[0], 1), 255)), axis=2).astype(np.uint8)
        if mask_array.ndim!=2:
            image_array[mask_array[:,:,0]==0, 3] = 0
        else: 
            image_array[np.expand_dims(mask_array, axis=2)[:,:,0]==0, 3] = 0 
    img_blend = Image.fromarray(image_array)
    return img_blend

def augment_module(mask_pil):
    method = random.choice([1, 2, 3])
    if method == 1:
        mask_pil = mask_pil.filter(ImageFilter.GaussianBlur(radius=1))
    if method == 2:
        mask_pil = mask_pil.filter(ImageFilter.BoxBlur(1))
    if method == 3:
        img = np.array(mask_pil)[:,:,0]
        rows, cols = img.shape
        img_output = np.zeros(img.shape, dtype=img.dtype)
        for i in range(rows):
            for j in range(cols):
                offset_x = int(5.0 * math.sin(2 * 3.14 * i / 180))
                offset_y = 0
                if j+offset_x < rows:
                    img_output[i,j] = img[i,(j+offset_x)%cols]
                else:
                    img_output[i,j] = 0
        mask_pil =  Image.fromarray(img_output)
    return mask_pil

class BarAssistant_B:
    def __init__(self, strength):
        self.s = strength

    def __call__(self, pipe_depth, pipe_paint, pipe_text2img, pipe_img2img, prompt, mask_pil, num_to_generate):
        bg_image = text2img(pipe_text2img, prompt, mask_pil.size, 1)[0]
        bg_image.save("output/bar_bg_image.png")
        if random.random() > 0.5:
            color_max = extract_colors(bg_image)
            img_blend = Image.blend(bg_image, mask_pil, 0.4)
            img_blend = crop_and_blend(img_blend, mask_pil, alpha_channel=None, color=color_max)
        else:
            color_max = extract_colors(bg_image)
            mask_pil = ImageOps.invert(mask_pil)
            img_blend = Image.blend(bg_image, mask_pil, 0.5)# bigger, mask 
            img_blend = crop_and_blend(img_blend, mask_pil, alpha_channel=None, color=color_max)
        img_blend.save("output/img_blend.png")
        images_rm_list = img2img(pipe_img2img, prompt, img_blend, num_to_generate, s=0.65) 

        return images_rm_list


class LineAssistant_B:
    def __init__(self):
        pass
    

    def attn_and_generate_by_prompt(self, pipe_text2img, prompt, object_prompt):
        generator = torch.Generator(device="cuda").manual_seed(random.randint(0,99999999)) 

        with torch.cuda.amp.autocast(dtype=torch.float16), torch.no_grad():
            with trace(pipe_text2img) as tc:
                out = pipe_text2img(prompt=prompt, width=512, height=512, guidance_scale=5.5, generator=generator)
                heat_map = tc.compute_global_heat_map()
                heat_map = heat_map.compute_word_heat_map(object_prompt)
        heat_map = heat_map.value.cpu().numpy()*255
        heat_map = heat_map.astype(np.uint8)
        heat_map_3d_arr = np.tile(heat_map[:, :, np.newaxis], (1, 1, 3))
        r = Image.fromarray(heat_map_3d_arr).resize((512,512)) # output_attn
        return np.array(r), out.images[0]

    def get_cotnext_by_attn(self, image, output_attn):
        image_arr = np.array(image.resize((512, 512)))
        bool_mask= np.where(output_attn[:,:,1]>125, output_attn[:,:,1], np.zeros_like(output_attn[:,:,1]))
        object_image = np.where(bool_mask[..., None], image_arr, np.zeros_like(image_arr))
        for channel in range(3):
            single_channel_array = np.array([])
            for i in range(object_image.shape[1]): # width?
                column = object_image[:, i, channel]
                new_column = np.concatenate((column[column==0], column[column!=0]))
                single_channel_array = np.vstack((single_channel_array, new_column)) if single_channel_array.size else new_column
            object_image[:,:, channel] = single_channel_array.T
        object_image = np.pad(object_image, ((0, 0), (0, 0), (0, 1)), 'constant', constant_values=255)
        # mask transparent
        object_image[object_image[:,:, 1]==0, 3] = 0
        context_image = Image.fromarray(object_image)
        return context_image

    def max_overlap(self, context_image):
        # img_pth = os.path.join(current_path, 'output\mask\line\mask1.png')
        line_image = PIL.Image.open("output\mask\line\mask1.png").convert('RGB').resize(context_image.size)
        line_image

        context_image_arr = np.array(context_image) # RGBA
        line_image_arr = np.array(line_image) # RGB 
        thresh_a = cv2.threshold(context_image_arr[:, :, 3], 0, 255, cv2.THRESH_BINARY)[1]
        thresh_b = cv2.threshold(line_image_arr[:, :, 2], 0, 255, cv2.THRESH_BINARY)[1]
        # print("initial overlapping: ", overlap_count(thresh_a, thresh_b))

        def overlap_count(thresh_a, thresh_b):
            overlap = cv2.bitwise_and(thresh_a, thresh_b)
            return cv2.countNonZero(overlap)

        # Define the overlap function
        def optimization_fun(params):
            M = np.float32([[0, 0, 0], [0, 0, 0]]) # afffine transformation matrix
            M[0,0] = params[0] 
            M[0,1] = params[1] 
            M[0,2] = params[2] 
            M[1,0] = params[3] 
            M[1,1] = params[4] 
            M[1,2] = params[5]
            img_affine = cv2.warpAffine(thresh_a, M, (thresh_a.shape[1], thresh_a.shape[0]))
            return -overlap_count(img_affine, thresh_b)
        
        row_idx, col_idx = np.nonzero(thresh_b)
        right_idx = np.argmax(col_idx)
        right_coor = (row_idx[right_idx], col_idx[right_idx])
        left_idx = np.argmin(col_idx)
        left_coor = (row_idx[left_idx], col_idx[left_idx])

        dy = np.abs(right_coor[0] - left_coor[0])
        dx = right_coor[1] - left_coor[1]
        angle = np.arctan2(dy, dx) * 180 / np.pi
        if angle > 0: 
            M = cv2.getRotationMatrix2D((0,thresh_a.shape[0]), angle/2, 1)
        if angle < 0: 
            M = cv2.getRotationMatrix2D((0,thresh_a.shape[0]), angle/2, 1)
            print(M)
            M[1,2]-=100
        res = minimize(optimization_fun, list(M.flatten()), bounds=[(0.8, 1.2), (-np.pi, np.pi), (-300, 300), (-np.pi, np.pi), (0.8, 1.2), (-300, 300)])

        img_affine = cv2.warpAffine(context_image_arr, np.array(res.x).reshape(2,3), (thresh_a.shape[1], thresh_a.shape[0]))
        return img_affine, thresh_b

    def fuse_chart_context(self, thresh_b,context_image, figure_size):
        context_image_arr = np.array(context_image)
        fuse_image_arr = np.where(thresh_b[..., None], context_image_arr[:,:,:3], np.ones_like(context_image_arr[:,:,:3])*255)
        fuse_image = Image.fromarray(fuse_image_arr)
        return fuse_image.resize(figure_size)
    
    def __call__(self, pipe_depth, pipe_paint, pipe_text2img, pipe_img2img, mask_pil, object_prompt, prompt, figure_size, mask_line_FLAG, num_to_generate):
        images_rm_list = []
        mask_pil = ImageOps.invert(augment_module(mask_pil).convert("RGB"))
        bg_image = text2img(pipe_text2img, prompt, mask_pil.size, 1)[0]
        images_pe = paint2img(pipe_paint, pipe_text2img, mask_pil,1, prompt)[0]
        img_crop = crop_and_blend(images_pe, mask_pil, alpha_channel=None)
        img_blend = Image.blend(bg_image,img_crop, 0.9)
        images_rm_list = img2img(pipe_img2img, prompt, img_blend, num_to_generate, s=0.65)
        return images_rm_list


class PieAssistant_B:
    def __init__(self):
        pass
    
    def draw_circle(self, ratio, margin=30):
        w, h = 512, 512
        shape = [(margin, margin), (w - margin, h - margin)]
        # creating new Image object
        img = Image.new("RGB", (w, h))
        # create pieslice image
        img1 = ImageDraw.Draw(img)
        img1.pieslice(shape, start = 0, end = int(360*ratio), fill ="white", outline ="white")
        return img
    
    def crop_as_sector(self, image, ratio, margin=30):
        pie_mask_circle = self.draw_circle(ratio, margin)
        image_array = np.array(image)
        mask_array = np.array(pie_mask_circle)
        result_array = np.where(mask_array == 0, 255, image_array)
        img_blend = Image.fromarray(result_array)
        return img_blend

    def __call__(self, pipe_depth, pipe_paint, pipe_text2img, pipe_img2img, mask_pil, object_prompt, prompt, figure_size, num_to_generate):
        
        images_rm_list = []

        nums_for_pe = 0
        nums_for_img2img = num_to_generate - nums_for_pe
        bg_image = text2img(pipe_text2img, prompt, mask_pil.size, 1)[0]

        # hope color in conspicuous object
        image = bg_removal(bg_image, current_path)
        image_arr = np.array(image)
        image_arr[image_arr[:,:,3]==0] = [255,255,255,0]
        image = Image.fromarray(image_arr[:,:,:3])
        color_max = extract_colors(image)


        img_blend = Image.blend(bg_image, mask_pil, 0.4)
        img_blend = crop_and_blend(img_blend, mask_pil, alpha_channel=None, color=color_max)
        img_blend.save("output/img_blend.png")
        img_tmp = img2img(pipe_img2img, prompt, img_blend, 1 , s=0.5)
        images_img2img = img2img(pipe_img2img, prompt, img_tmp, nums_for_img2img , s=0.55)  if nums_for_img2img != 0 else None
        
        for images in [images_img2img]:
            if isinstance(images, list):
                for img in images:
                    img.save("output/kankan.png")
                    images_rm_list.append(img)        
        
        return images_rm_list


class ScatterAssistant_B:
    def __init__(self):
        pass
    
    def __call__(self, pipe_depth, pipe_paint, pipe_text2img, pipe_img2img, mask_pil, object_prompt, prompt, figure_size, num_to_generate):
        images_rm_list = []

        nums_for_pe = 0
        nums_for_img2img = num_to_generate - nums_for_pe
        bg_image = text2img(pipe_text2img, prompt, mask_pil.size, 1)[0]

        # hope color in conspicuous object
        image = bg_removal(bg_image, current_path)
        image_arr = np.array(image)
        image_arr[image_arr[:,:,3]==0] = [255,255,255,0]
        image = Image.fromarray(image_arr[:,:,:3])
        color_max = extract_colors(image)


        img_blend = Image.blend(bg_image, mask_pil, 0.4)
        img_blend = crop_and_blend(img_blend, mask_pil, alpha_channel=None, color=color_max)
        img_blend.save("output/img_blend.png")
        img_tmp = img2img(pipe_img2img, prompt, img_blend, 1 , s=0.5)
        images_img2img = img2img(pipe_img2img, prompt, img_tmp, nums_for_img2img , s=0.55)  if nums_for_img2img != 0 else None
        
        for images in [images_img2img]:
            if isinstance(images, list):
                for img in images:
                    images_rm_list.append(img)        
        return images_rm_list


    

