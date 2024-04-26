import sys
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import math
from PIL import Image, ImageDraw, ImageOps, ImagePath
current_path = os.getcwd()

def table2img_scatter(x, y, z, title, y_limit, aspect_ratio):
    plt.rcParams['svg.fonttype'] = 'none'
    plt.rcParams['text.usetex'] = 'False'
    fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
    if y_limit != None:
        ax.set_ylim(y_limit)
    
    if len(z)==0:
        z = [1]*len(x)
        ax.scatter(x, y, s=[value * 1200 for value in z], c='skyblue')
    else:
        ax.scatter(x, y, s=[value * 1200 for value in z], c='skyblue')
    # DEFAULT: start_angle = 0, counterclockwise
    
    # ax.set_xlabel("Year Season")
    # ax.set_ylabel("Goals scored")

    ax.set_title(title)
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    four_corners = [x_min, x_max, y_min, y_max]
    print(x_min, x_max, y_min, y_max)
    ax.set_xlim([x_min-1, x_max+1]) ####################################
    ax.set_ylim([y_min-15, y_max+20]) #####################################
    # ax.axis('off')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.tight_layout()
    fig.savefig('output/preview/scatter_preview.png', dpi=fig.dpi)
    fig.savefig('frontend/src/assets/preview/scatter_preview.png', dpi=fig.dpi)
    fig.savefig("frontend/src/assets/preview/plot.svg", transparent = True, format="svg", dpi=fig.dpi)
    return 'frontend/src/assets/preview/scatter_preview.png'

def img2mask_scatter(x, y, z, y_limit, aspect_ratio):
    mask_path_foreground = []
    mask_path_background = []

    plt.style.use('dark_background')
    if len(z)==0:
        z = [1]*len(x)

    # single
    colors_list = ["black"] * len(x)
    for i in range(len(x)):
        colors_list[i] = "white"
        fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
        ax.scatter(x, y, s=[value * 1200 for value in z], c=colors_list)
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        four_corners = [x_min, x_max, y_min, y_max]
        ax.set_xlim([x_min-1, x_max+1]) ####################################
        ax.set_ylim([y_min-15, y_max+20]) #####################################
        ax.axis('off')
        plt.tight_layout()
        fig.savefig('output/mask/scatter/foreground/mask_'+str(i)+'.png', dpi=fig.dpi)
        fig.savefig('frontend/src/assets/mask/scatter/foreground/mask_'+ str(i) +'.png', dpi=fig.dpi)
        mask_path_foreground.append('src/assets/mask/scatter/foreground/mask_'+ str(i) +'.png')
        colors_list[i] = "black"
    
    # all
    fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
    scatter_plot = ax.scatter(x, y, s=[value * 1200 for value in z], c='white')
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    four_corners = [x_min, x_max, y_min, y_max]
    ax.set_xlim([x_min-1, x_max+1]) ####################################
    ax.set_ylim([y_min-15, y_max+20]) #####################################
    ax.axis('off')
    plt.tight_layout()
    fig.savefig('output/mask/scatter/foreground/mask_all.png', dpi=fig.dpi)
    fig.savefig('frontend/src/assets/mask/scatter/foreground/mask_all.png', dpi=fig.dpi)
    mask_path_foreground.append('src/assets/mask/scatter/foreground/mask_all.png')
        
    # background 反过来
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
    ax.scatter(x, y, s=[value * 1200 for value in z], c='black')
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    four_corners = [x_min, x_max, y_min, y_max]
    ax.set_xlim([x_min-1, x_max+1]) ####################################
    ax.set_ylim([y_min-15, y_max+20]) #####################################
    ax.axis('off')
    plt.tight_layout()
    fig.savefig('output/mask/scatter/background/mask_all.png', dpi=fig.dpi)
    fig.savefig('frontend/src/assets/mask/scatter/background/mask_all.png', dpi=fig.dpi)
    mask_path_background.append('src/assets/mask/scatter/background/mask_all.png')

    return mask_path_foreground, mask_path_background


    # 暂时不用scatter的mask
    # fig_size = fig.canvas.get_width_height()
    # bg = Image.new("RGB", fig_size, "black")
    # draw = ImageDraw.Draw(bg)

    # # create line image
    # for i in range(len(pos_pix)-1):
    #     draw.line([tuple(pos_pix[i]), tuple(pos_pix[i+1])], fill ="white", width = 20)    
    # bg.save('output/mask/line/mask1.png')
    # bg_reverse = ImageOps.invert(bg)
    # bg_reverse.save('output/mask/line/mask2.png')


# # user defined data
# x = np.random.rand(5)
# y = np.random.rand(5)
# z = np.random.rand(5) # or empty list []
# a = {"x": ["04/05", "08/09", "12/13", "16/17", "20/21"], "y": [1, 38, 60, 54, 38], "z": [0.1, 0.7, 1.2, 1.0, 0.8], "title": "Goals scored by Linel Messi for FC Barcelona in all competitions"}
# x = a["x"]
# y = a["y"]
# z = a["z"]
# z = [1, 7, 12, 10, 8]
# z = [value**2 for value in z]
# title = a["title"]
# aspect_ratio = (10, 8)
# ## get four corners list
# four_corners=None
# # if four_corners==None:
# #     four_corners = [min(x)-1, max(x)+1, min(y)-1, max(y)+1]
# y_limit = None#(-3,10)

# table2img_scatter(x, y, z, title, y_limit, aspect_ratio)
# img2mask_scatter(x, y, z, y_limit, aspect_ratio)

