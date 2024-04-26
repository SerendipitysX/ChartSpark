from typing import Any
from PIL import Image, ImageDraw, ImageFilter
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
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)
from mask.bg_removal import bg_removal
from generation.model_utils import load_model_from_config, get_attn_mask
from grid.grid_compile import *

## ==================== Load model ====================
# Paths and prompt
# device = "cuda"
# config="generation/config/v1-inference.yaml"
# ckpt = "generation/model/sd-v1-4-full-ema.ckpt"


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

def crop_and_blend(bg_image_pil, mask_pil, alpha_channel=None):
    image_array = np.array(bg_image_pil)
    mask_array = np.array(mask_pil)
    if alpha_channel is None:
        if mask_array.ndim!=2:
            image_array = np.where(mask_array == 0, 255, image_array)
        else:
            image_array = np.where(np.expand_dims(mask_array, axis=2) == 0, 255, image_array)
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

class BarAssistant:
    def __init__(self, strength):
        self.s = strength

    def add_margin(self, img, size=(512,512)):
        background = Image.new("RGB", size, "white")

        x = (background.width - img.width) // 2
        y = (background.height - img.height) // 2

        image_arr = np.array(img)
        image_arr[image_arr[:,:,3]==0] = [255,255,255,0]
        img = Image.fromarray(image_arr)
        background.paste(img, (x, y)) 
        return background

    def prepare_grid(self, img_removal):
        split_num = 5
        # get box of correct object and get the total_h(h_total)
        img_removal_correct, h_total, (h_highest, w, channel) = get_box_img(img_removal)
        # cut
        grid_dict, h_grid = get_grid(img_removal_correct, h_total)
        # get similarity matrix
        sim_matrix = np.ones((split_num, split_num))
        sort_idx_array, sim_mean = ssim_matrix_compute(grid_dict, sim_matrix)
        # show all grid and meta_grid
        grid_meta, grid_img_list = get_grid_meta(grid_dict, sort_idx_array)
        return grid_img_list, img_removal_correct, sort_idx_array, h_highest,h_grid
    
    def get_all_bar_element(self, grid_img_list, h_list, img_removal_correct, sort_idx_array, h_highest,h_grid):
        img_pth = os.path.join(os.getcwd(), 'output/mask/bar/foreground/mask_all.png')
        mask_image = PIL.Image.open(img_pth).convert('RGB')
        init_image = Image.new("RGBA", mask_image.size)
        imgray = cv2.cvtColor(np.array(mask_image), cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 30, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print("hlist::::", h_list)
        for i in range(len(contours)):
            x,y,w,h = cv2.boundingRect(contours[i])
            print(i, h)
            w = grid_img_list[0].size[0]
            if np.abs(h-max(h_list)) < 5:
                print('----------')
                init_image.paste(Image.fromarray(img_removal_correct), (x,y-(h_highest-max(h_list))))
            else:
                new_bar = grid_compile(grid_img_list, sort_idx_array, h, h_highest, h_grid, w)
                init_image.paste(new_bar, (x, y))
            # init_image.save("output/bar"+str(i)+".png")
        init_image_arr = np.array(init_image)
        init_image_arr[init_image_arr[:,:,3]==0] = [255,255,255,0]
        init_image = Image.fromarray(init_image_arr[:,:,:3])
        # init_image.save("output/11111111111.png")
        a = init_image.convert("RGB")
        a.save("output/2222222222.png")
        return init_image.convert("RGB")

    def __call__(self, pipe_depth, pipe_paint, pipe_text2img, pipe_img2img, prompt, bar_mask, num_to_generate, mask_single_FLAG):
        images_rm_list = []
        bar_mask = augment_module(bar_mask).convert("RGB")
        # nums_for_pe = 0 if num_to_generate == 1 or num_to_generate % 2 == 1 else num_to_generate // 2
        nums_for_pe = 0
        nums_for_depth = num_to_generate - nums_for_pe
        if mask_single_FLAG:
            # method1: PE
            images_pe = paint2img(pipe_paint, pipe_text2img, bar_mask, nums_for_pe, prompt) if nums_for_pe != 0 else None
            # method2: depth
            # images_depth2img = depth2img(pipe_depth, prompt, bar_mask, num_images=nums_for_depth, s = 0.95) if nums_for_depth != 0 else None
            # using FE ======
            images_depth2img = text2img(pipe_text2img, prompt, bar_mask.size, nums_for_depth)
            imgray = cv2.cvtColor(np.array(bar_mask), cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(imgray, 30, 255, 0)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cntr in contours:
                x,y,w,h = cv2.boundingRect(cntr)
            # ========
            # remove background
            for images in [images_pe, images_depth2img]:
                if isinstance(images, list):
                    for img in images:
                        # img_RGBA = bg_removal(img, current_path)
                        img_RGBA = bg_removal(img, current_path).resize((w, h))
                        element = crop_element_from_RGBA(img_RGBA).resize((w, h))
                        # refine again ----
                        ele_img = self.add_margin(element, size=(512,512))
                        # ele_img.save("output/kankan.png")
                        ele_img = img2img(pipe_img2img, prompt, ele_img, 1, s=0.65)[0]
                        img_RGBA = bg_removal(ele_img, current_path)
                        element = crop_element_from_RGBA(img_RGBA, mask_single_FLAG)
                        # ----
                        images_rm_list.append(element)        
        else:
            # method1: PE
            images_pe = paint2img(pipe_paint, pipe_text2img, bar_mask, nums_for_pe, prompt) if nums_for_pe != 0 else None
            if isinstance(images_pe, list):
                for img in images_pe:
                    img_RGBA = bg_removal(img, current_path)
                    element = crop_element_from_RGBA(img_RGBA)
                    images_rm_list.append(element)        
            # method2: depth
            with open('output/mask/bar/bar_heights.json', 'r') as f:
                h_list = json.load(f)
            # step2: get the anchor (highest transformed element)
            mask_pil = Image.open("output/mask/bar/mask_highest.png")
            for i in range(nums_for_depth):
                image_highest = depth2img(pipe_depth, prompt, mask_pil, num_images=1, s = 0.95)[0]
                # using FE ======
                image_highest = text2img(pipe_text2img, prompt, mask_pil.size, 1)[0]
                imgray = cv2.cvtColor(np.array(mask_pil), cv2.COLOR_BGR2GRAY)
                ret, thresh = cv2.threshold(imgray, 30, 255, 0)
                contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for cntr in contours:
                    x,y,w,h = cv2.boundingRect(cntr)
                # ========
                # img_removal = bg_removal(image_highest, current_path)
                img_removal = bg_removal(image_highest, current_path).resize((w, h))
                img_removal = crop_element_from_RGBA(img_removal).resize((w, h))
                img_removal.save("output/img_removal.png")
                # step3: prepare grid
                grid_img_list, img_removal_correct, sort_idx_array, h_highest,h_grid = self.prepare_grid(img_removal)
                # step4: get all_bar_element
                all_bar_element = self.get_all_bar_element(grid_img_list, h_list, img_removal_correct, sort_idx_array, h_highest,h_grid)
                all_bar_element = img2img(pipe_img2img, prompt, all_bar_element, 1, s=0.65)[0]
                img_RGBA = bg_removal(all_bar_element, current_path)
                element = crop_element_from_RGBA(img_RGBA, mask_single_FLAG)
                images_rm_list.append(element)
        return images_rm_list

class LineAssistant:
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

    ## ===== step2. 通过attn，得到集中的纹理 version1
    # image_arr = np.array(image)
    # bool_mask= np.where(output_attn[:,:,1]<120, output_attn[:,:,1], np.zeros_like(output_attn[:,:,1]))
    # context_image = np.where(bool_mask[..., None], image_arr, np.zeros_like(image_arr))
    # # extend dim for RGBA, all is 255 (not transparent)
    # context_image = np.pad(context_image, ((0, 0), (0, 0), (0, 1)), 'constant', constant_values=255)
    # # mask transparent
    # context_image[context_image[:,:, 1]==0, 3] = 0
    # context_image = Image.fromarray(context_image).resize((576,432))
    #### 通过attn，得到集中的纹理 version1 + 像素下移
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

    ## ===== step3. affine transfomation to maximize overlapping
    # load two img
    def max_overlap(self, context_image):
        # img_pth = os.path.join(current_path, 'output\mask\line\mask1.png')
        line_image = PIL.Image.open("D:\speak\output\mask\line\mask1.png").convert('RGB').resize(context_image.size)
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
            M[0,0] = params[0] # 放缩和旋转的元素。表示在x轴上的放缩系数
            M[0,1] = params[1] # 放缩和旋转的元素。表示在x轴上的旋转系数
            M[0,2] = params[2] # 表示在x轴上的平移量
            M[1,0] = params[3] # 放缩和旋转的元素。表示在y轴上的旋转系数
            M[1,1] = params[4] # 放缩和旋转的元素。表示在y轴上的放缩系数
            M[1,2] = params[5] # 表示在y轴上的平移量
            img_affine = cv2.warpAffine(thresh_a, M, (thresh_a.shape[1], thresh_a.shape[0]))
            return -overlap_count(img_affine, thresh_b)
        
        # 确定optimization的初始参数
        # 根据mask算line的斜率
        row_idx, col_idx = np.nonzero(thresh_b)
        right_idx = np.argmax(col_idx)
        right_coor = (row_idx[right_idx], col_idx[right_idx])
        left_idx = np.argmin(col_idx)
        left_coor = (row_idx[left_idx], col_idx[left_idx])
        # 计算斜率，没错, 记住这个是左上角。矩阵
        dy = np.abs(right_coor[0] - left_coor[0])
        dx = right_coor[1] - left_coor[1]
        angle = np.arctan2(dy, dx) * 180 / np.pi
        if angle > 0: 
            M = cv2.getRotationMatrix2D((0,thresh_a.shape[0]), angle/2, 1)
        if angle < 0: 
            M = cv2.getRotationMatrix2D((0,thresh_a.shape[0]), angle/2, 1)
            print(M)
            M[1,2]-=100
        # Run the optimization
        res = minimize(optimization_fun, list(M.flatten()), bounds=[(0.8, 1.2), (-np.pi, np.pi), (-300, 300), (-np.pi, np.pi), (0.8, 1.2), (-300, 300)])

        # Print the result
        # print("Optimal overlap ratio:", -res.fun)
        # print(res.x)
        img_affine = cv2.warpAffine(context_image_arr, np.array(res.x).reshape(2,3), (thresh_a.shape[1], thresh_a.shape[0]))
        return img_affine, thresh_b

    ## ===== step4. fusing 
    def fuse_chart_context(self, thresh_b,context_image, figure_size):
        context_image_arr = np.array(context_image)
        fuse_image_arr = np.where(thresh_b[..., None], context_image_arr[:,:,:3], np.ones_like(context_image_arr[:,:,:3])*255)
        fuse_image = Image.fromarray(fuse_image_arr)
        return fuse_image.resize(figure_size)
    
    def __call__(self, pipe_depth, pipe_paint, pipe_text2img, pipe_img2img, mask_pil, object_prompt, prompt, figure_size, mask_line_FLAG, num_to_generate):
        images_rm_list = []
        mask_pil = augment_module(mask_pil).convert("RGB")
        if mask_line_FLAG:
            try:
                nums_for_img2img = 1 if num_to_generate == 1 or num_to_generate % 2 == 1 else num_to_generate // 2
                nums_for_depth = num_to_generate - nums_for_img2img
                bg_image = text2img(pipe_text2img, prompt, mask_pil.size, 1)[0]
                img_blend = crop_and_blend(bg_image, mask_pil)
                # method1: img2img
                images_img2img = img2img(pipe_img2img, prompt, img_blend, nums_for_img2img, s=0.5) if nums_for_img2img != 0 else None
                # method2: depth
                images_depth2img = depth2img(pipe_depth, prompt, img_blend, num_images=nums_for_depth, s = 0.88) if nums_for_depth != 0 else None
                # remove background
                for images in [images_img2img, images_depth2img]:
                    if isinstance(images, list):
                        for img in images:
                            element = bg_removal(img, current_path)
                            # element = crop_element_from_RGBA(img_RGBA)
                            # element.save("output/kankan.png")
                            images_rm_list.append(element)        
                return images_rm_list
            except:
                # output_attn, image = self.attn_and_generate_by_prompt(pipe_text2img, prompt, object_prompt) # only 512*512
                # context_image = self.get_cotnext_by_attn(image, output_attn)
                # img_affine, thresh_b = self.max_overlap(context_image)
                # fuse_image = self.fuse_chart_context(thresh_b,img_affine, figure_size)
                # fuse_image = img2img(pipe_img2img, object_prompt, fuse_image, 1,s =0.85)
                # return fuse_image[0]
                bg_image = text2img(pipe_text2img, prompt, mask_pil.size, 1)[0]
                img_blend = crop_and_blend(bg_image, mask_pil, alpha_channel=None)
                images_depth2img = depth2img(pipe_depth, prompt, img_blend, num_images=nums_for_depth, s = 0.9) if nums_for_depth != 0 else None

        else:
            bg_image = text2img(pipe_text2img, prompt, mask_pil.size, 1)[0]
            images_pe = paint2img(pipe_paint, pipe_text2img, mask_pil, 1, prompt)[0]
            # RGB bg_image
            img_blend1 = crop_and_blend(bg_image, mask_pil, alpha_channel=None).convert("RGB")
            # RGBA pe_image
            img_pe_r = bg_removal(images_pe, current_path)
            img_blend = Image.alpha_composite(img_blend1.convert("RGBA"), img_pe_r)
            img_blend = img_blend.convert("RGB")
            images_img2img = img2img(pipe_img2img, prompt, img_blend, num_to_generate, s=0.58)

            mask_array = np.array(mask_pil)
            if isinstance(images_img2img, list):
                for img in images_img2img:
                    # element = crop_and_blend(img, mask_pil, alpha_channel="yes")
                    # element.save("output/kankan1.png")
                    # images_rm_list.append(element)        
                    img_RGBA = bg_removal(img, current_path)
                    image_array = np.array(img_RGBA)
                    image_array[mask_array[:,:,0]==0, 3] = 0 
                    element = Image.fromarray(image_array)
                    element = crop_element_from_RGBA(element)
                    element.save("output/kankan.png")
                    images_rm_list.append(element)        
                return images_rm_list


class PieAssistant:
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
        # mask_pil = augment_module(mask_pil).convert("RGB")
        mask_pil = mask_pil.convert("RGB")
        # nums_for_depth = num_to_generate if num_to_generate == 1 or num_to_generate % 2 == 1 else num_to_generate // 2
        nums_for_depth = num_to_generate
        nums_for_pe = num_to_generate - nums_for_depth
        circle = Image.open("output/mask/pie/foreground/mask_all.png").convert("RGB")

        # initial step: create bg_image
        if os.path.isfile("output/mask/pie/foreground/pie_bg_temp.png"):
            bg_image_tmp = Image.open("output/mask/pie/foreground/pie_bg_temp.png").convert("RGB")
            bg_image = img2img(pipe_img2img, prompt, bg_image_tmp, 1, s=0.9)[0]
        else:
            bg_image = text2img(pipe_text2img, prompt, mask_pil.size, 1)[0]
            bg_image.save("output/mask/pie/foreground/pie_bg_temp.png")
        # method1: depth
        img_blend_depth = crop_and_blend(bg_image, mask_pil)
        images_depth2img = depth2img(pipe_depth, prompt, img_blend_depth, num_images=nums_for_depth, s = 0.9) if nums_for_depth != 0 else None
        # method2: pe
        if np.random.rand() > 0.85:
            img_blend_pe = crop_and_blend(bg_image_pil=bg_image, mask_pil=circle, alpha_channel=None)
            image_array = np.array(img_blend_pe.convert("RGB"))
            mask_array = np.array(mask_pil)
            image_array = np.concatenate((image_array, np.full((mask_pil.size[1], mask_pil.size[0], 1), 255)), axis=2).astype(np.uint8)
            image_array[mask_array[:,:,-1]==255, :3] = 255
            img_blend_pe = Image.fromarray(image_array)
            images_pe = paint2img(pipe_paint, pipe_text2img, mask_pil, nums_for_pe, prompt, init_img = img_blend_pe) if nums_for_pe != 0 else None
        else:
            images_pe = paint2img(pipe_paint, pipe_text2img, mask_pil, nums_for_pe, prompt) if nums_for_pe != 0 else None
        # remove background
        for images in [images_depth2img, images_pe]:
            if isinstance(images, list):
                for img in images:
                    img_RGBA = crop_and_blend(img, mask_pil, alpha_channel="yes")
                    element = crop_element_from_RGBA(img_RGBA)
                    images_rm_list.append(element)        
        return images_rm_list


class ScatterAssistant:
    def __init__(self):
        pass

    def get_size_from_mask(self, mask_pil):
        mask_arr = np.array(mask_pil)
        imgray = cv2.cvtColor(mask_arr, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 30, 255, 0)
        cv2.imwrite('output/grid/thresh.png', thresh)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 1:
            for cntr in contours:
                x,y,w,h = cv2.boundingRect(cntr)
            return x,y,w,h
        else:
            x_list, y_list, w_list, h_list = [], [], [], []
            for cntr in contours:
                x,y,w,h = cv2.boundingRect(cntr)
                x_list.append(x)
                y_list.append(y)
                w_list.append(w)
                h_list.append(h)         
            return x_list, y_list, w_list, h_list
        
    def __call__(self, pipe_depth, pipe_paint, pipe_text2img, pipe_img2img, mask_pil, object_info, prompt, figure_size, mask_single_FLAG, num_to_generate):
        images_rm_list = []
        x,y,w,h = self.get_size_from_mask(mask_pil)
        if mask_single_FLAG:
            images_text2img = text2img(pipe_text2img, prompt, mask_pil.size, num_to_generate)
            for i in range(num_to_generate):
                img_removal = bg_removal(images_text2img[i], current_path)
                element = crop_element_from_RGBA(img_removal, mask_single_FLAG).resize((int(w), int(h)))
                images_rm_list.append(element)
        else:
            images_text2img = text2img(pipe_text2img, prompt, mask_pil.size, num_to_generate)
            for i in range(num_to_generate):
                new_pil = Image.new("RGBA", mask_pil.size)
                img_removal = bg_removal(images_text2img[i], current_path)
                for j in range(len(x)):
                    element = crop_element_from_RGBA(img_removal, mask_single_FLAG).resize((w[j], h[j]))
                    new_pil.paste(element, box=(x[j], y[j]))
                new_pil = crop_element_from_RGBA(new_pil, mask_single_FLAG)
                images_rm_list.append(new_pil)
        return images_rm_list

     

# try lineassistant
# from diffusers import DiffusionPipeline,StableDiffusionDepth2ImgPipeline,StableDiffusionImg2ImgPipeline,StableDiffusionPipeline
# model_id = "C:/Users/wangb/.cache/huggingface/diffusers/models--runwayml--stable-diffusion-v1-5/snapshots/39593d5650112b4cc580433f6b0435385882d819"
# model_depth = "C:/Users/wangb/.cache/huggingface/diffusers/models--stabilityai--stable-diffusion-2-depth/snapshots/d41a0687231847e8bd55f43fb1f576afaeefef19"
# model_paint = "C:/Users/wangb/.cache/huggingface/diffusers/models--Fantasy-Studio--Paint-by-Example/snapshots/351e6427d8c28a3b24f7c751d43eb4b6735127f7"
# pipe_text2img = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16,cache_dir="models",local_files_only=True).to("cuda")
# pipe_img2img = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")
# line = LineAssistant()
# object_prompt = "tree branch"
# prompt = "tree branch, horizontally, slender"
# # img_pth = os.path.join(current_path, 'output\mask\line\mask1.png')
# line_image = PIL.Image.open("D:\speak\output\mask\line\mask1.png").convert('RGB')
# print(line_image.size)
# fuse_img = line(object_prompt, prompt, pipe_img2img, pipe_text2img, line_image.size)
# fuse_img.save("xxxxxxxxxxxxx.png")