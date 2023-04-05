# Importing the modules
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
from PIL import Image
import cv2
# import extcolorspip
from colormap import rgb2hex
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from sklearn.cluster import KMeans
from tqdm import tqdm
import os
current_path = os.path.dirname(os.getcwd())


from matplotlib.colors import ListedColormap

def draw_colorbar(color_list, count_list):
    color_list_hex = [rgb2hex(i[0], i[1], i[2]) for i in color_list]
    count_array = np.array(count_list)

    fig, ax = plt.subplots()
    fig.set_facecolor('black')
    plt.imshow(np.repeat(np.arange(len(color_list_hex)), count_array).reshape(1, -1),
            cmap=ListedColormap(color_list_hex), # the given list of colors
            aspect=count_array.sum()/10)  # 1:10 aspect ratio for the image
    plt.axis('off')
    plt.savefig('output/mask/colorbar.jpg')
    return

def get_image_colors(image, scale):
    if type(image) == str:
        with Image.open(image).convert('RGB') as im:
            total_pixels = im.size[0] * im.size[1]
            colors = im.getcolors(total_pixels)
            large_colors = []
            for color in colors:
                if color[0] > total_pixels*scale and color[1] != (255, 255, 255) and color[1] != (255, 255, 255):  # 如果某颜色占该图片的总像素超过100
                    large_colors.append(color)
            large_colors = sorted(large_colors, key=lambda t: t[0], reverse=True)
            color_list = [color[1] for color in large_colors]
            count_list = [color[0] for color in large_colors]
            return color_list, count_list
    else:
        im = image.convert('RGB')
        total_pixels = im.size[0] * im.size[1]
        colors = im.getcolors(total_pixels)
        large_colors = []
        for color in colors:
            if color[0] > total_pixels*scale and color[1] != (255, 255, 255) and color[1] != (255, 255, 255):  # 如果某颜色占该图片的总像素超过100
                large_colors.append(color)
        large_colors = sorted(large_colors, key=lambda t: t[0], reverse=True)
        color_list = [color[1] for color in large_colors]  # 存储颜色的列表
        count_list = [color[0] for color in large_colors]  # 存储数量的列表
        draw_colorbar(color_list, count_list)
        return color_list, count_list


# color_list, count_list = get_image_colors(current_path+'/data/bar1.png', scale=0.01)