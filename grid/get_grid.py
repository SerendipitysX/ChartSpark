import math
import sys
import cv2
from PIL import Image
import PIL
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
current_path = os.getcwd()

split_num = 5

def image_grid(imgs, rows, cols):
    # imgs is a list containing several PIL objects
    assert len(imgs) == rows * cols

    w, h = imgs[0].size
    grid = PIL.Image.new('RGBA', size=(cols * w, rows * h))
    grid_w, grid_h = grid.size

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid

def approximate_gcd(nums):
    total_remainders = {}
    if type(nums)==int:
        magic_thr = nums//split_num
    else:
        max_num = max(nums)
        min_num = min(nums)
        magic_thr = min_num if min_num<=20 else max_num//split_num
    return magic_thr

def get_box_img(image):
    '''get box of correct object and get the total_h(h_total)'''
    img_removal = np.array(image)
    imgray = cv2.cvtColor(img_removal, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 30, 255, 0)
    cv2.imwrite('output/grid/thresh.png', thresh)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    left, top, right, bottom = image.width, image.height, 0, 0 
    for x in range(image.width): 
        for y in range(image.height): 
            if image.getpixel((x, y))[3] != 0: 
                left = min(left, x) 
                top = min(top, y) 
                right = max(right, x) 
                bottom = max(bottom, y) 
    y_gen = top
    x_gen = left
    h_total = bottom - top
    w_gen = right- left

    img_removal_correct = img_removal[y_gen:y_gen+h_total,x_gen:x_gen+w_gen]
    cv2.imwrite('output/grid/img_removal_correct.png', cv2.cvtColor(img_removal_correct, cv2.COLOR_RGB2BGRA))
    return img_removal_correct, h_total, img_removal_correct.shape

def get_grid(img_removal_correct, h_total):
    grid_h = approximate_gcd(h_total)
    grid_dict = {}
    offset = 0
    for i in range(split_num): # (134, 34, 4)
        grid = img_removal_correct[offset:offset+grid_h, : , :]
        grid_dict[str(i)] = Image.fromarray(grid)
        offset += grid_h
    return grid_dict, grid_h

def compare_images_ssim(imageA, imageB):
    imageA = cv2.cvtColor(np.array(imageA), cv2.COLOR_RGB2GRAY)
    imageB = cv2.cvtColor(np.array(imageB), cv2.COLOR_RGB2GRAY)
    return(ssim(imageA, imageB))

def ssim_matrix_compute(grid_dict, sim_matrix):
    for i in range(split_num):
        for j in range(i + 1, split_num):
            image1 = grid_dict[str(i)]
            image2 = grid_dict[str(j)]
            similarity = compare_images_ssim(image1, image2)
            sim_matrix[i,j], sim_matrix[j,i] = similarity, similarity
    sim_mean = np.mean(sim_matrix, axis=1)
    sort_idx_array = np.argsort(sim_mean)[::-1] # descend
    return sort_idx_array, sim_mean

# show all grid and meta_grid
def get_grid_meta(grid_dict, sort_idx_array):
    # ssim larger is more similar
    '''show all grid and meta_grid'''
    grid_img_list = list(grid_dict.values())
    # draw
    all_grid = image_grid(grid_img_list, 1, split_num)
    all_grid.save('output/grid/all_grid.png')
    grid_img_list[sort_idx_array[0]].save('output/grid/grid_meta.png')
    # get_grid_meta
    grid_meta = grid_img_list[sort_idx_array[0]]
    return grid_meta, grid_img_list
