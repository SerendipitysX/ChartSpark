import sys
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import math
from PIL import Image, ImageDraw, ImageOps, ImagePath
current_path = os.getcwd()
color_bg = "black"

def table2img_bar(x, height, labels, aspect_ratio, title, y_limit=None, bar_width=0.8):
    fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
    plt.bar(labels, height, width=bar_width, color="skyblue")
    plt.xticks(labels)
    ax.set_title(title)
    if y_limit != None:
        ax.set_ylim(y_limit)
    # ax.axis('off')
    ax.set_xlabel("age group")
    ax.set_ylabel("time hours")
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    fig.savefig('output/preview/bar_preview.png', dpi=fig.dpi)
    fig.savefig('D:/speak/frontend/src/assets/preview/bar_preview.png', dpi=fig.dpi)
    return 'D:/speak/frontend/src/assets/preview/bar_preview.png'

def img2mask_bar(x, height, labels, aspect_ratio, y_limit=None, bar_width=1.5):
    # get the mask
    # reverse
    fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
    bars = plt.bar(labels, height, width=bar_width, color='black')
    plt.xticks(labels)
    if y_limit != None:
        ax.set_ylim(y_limit)
    ax.axis('off')
    fig.savefig('output/mask/bar/mask_reverse.png', dpi=fig.dpi)
    # allhuandiannaoqule
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
    bars = plt.bar(labels, height, width=bar_width, color='white')
    plt.xticks(labels)
    if y_limit != None:
        ax.set_ylim(y_limit)
    ax.axis('off')
    fig.savefig('output/mask/bar/mask_all.png', dpi=fig.dpi)
    # get the mask
    # single
    ww, hh = fig.canvas.get_width_height()
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    bar_heights = [int(bar.get_window_extent(r).height) for bar in bars]
    bar_width = int(bars[0].get_window_extent(r).width)
    max_bar_height = max(bar_heights)
    # print(max_bar_height)
            

	# ------------------------------- crop -------------------------
    if max_bar_height < 512:
        bg = Image.new("RGB", (512, 512), color_bg)
    else:
        print('max_bar_height > 512')
        print(ww, hh)
    i = 0
    for bar_h in bar_heights:
        draw = ImageDraw.Draw(bg)
        shape = [(512/2-bar_width/2, 512/2-bar_h/2), (512/2+bar_width/2, 512/2+bar_h/2)] # lefttop_xy, rightbottom_xy
        draw.rectangle(shape, fill='white')
        bg.save('output/mask/bar/mask_' + str(i) + '.png')
        i += 1

    if max_bar_height < 512:
        bg = Image.new("RGB", (512, 512), color_bg)
    else:
        print('max_bar_height > 512')
    draw = ImageDraw.Draw(bg)
    shape = [(512/2-bar_width/2, 512/2-max_bar_height/2), (512/2+bar_width/2, 512/2+max_bar_height/2)] # lefttop_xy, rightbottom_xy
    draw.rectangle(shape, fill='white')
    bg.save('output/mask/bar/mask_highest.png')
    plt.style.use('default')



    plt.style.use('default')

    return bar_heights


# user defined data
a = {"x": [2000, 2004,  2008,  2012], "y": [672718297, 677741808, 713618164, 707086427], "title": "Global agricultural land use by cereal"}
a = {"x": ["15 to 19 years", "25 to 34 years", "45 to 54 years", "65 to 74 years"], "y": [0.16, 0.13, 0.26, 0.49], "title": "Average daily time spent reading per capita in US in 2021"}
height = a["y"]
labels = a["x"]
x = np.arange(len(labels))
# aspect_ratio = [(1,1), (3,2),     (4, 3), (5, 4)]
aspect_ratio = [(5,5), (5.5,3.7), (4, 3), (5, 4)]
# y_limit = (572718297, 751403440) # (-3, 50)
y_limit = None
bar_width = 0.8
title = a["title"]


table2img_bar(x, height, labels, aspect_ratio[3], title, y_limit, bar_width)
img2mask_bar(x, height, labels, aspect_ratio[3], y_limit, bar_width)


# def img2mask_bar(x, height, labels, aspect_ratio, y_limit=None):
#     # get the mask
#     # reverse
#     fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
#     bars = plt.bar(x, height, color='black')
#     plt.xticks(x, labels)
#     if y_limit != None:
#         ax.set_ylim(y_limit)
#     ax.axis('off')
#     fig.savefig('output/mask/bar/mask_reverse.png', dpi=fig.dpi)
#     # allhuandiannaoqule
#     plt.style.use('dark_background')
#     fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
#     bars = plt.bar(x, height, color='white')
#     plt.xticks(x, labels)
#     if y_limit != None:
#         ax.set_ylim(y_limit)
#     ax.axis('off')
#     fig.savefig('output/mask/bar/mask_all.png', dpi=fig.dpi)
#     # get the mask
#     # single
#     ww, hh = fig.canvas.get_width_height()
#     fig.canvas.draw()
#     r = fig.canvas.get_renderer()
#     bar_heights = [int(bar.get_window_extent(r).height) for bar in bars]
#     bar_width = int(bars[0].get_window_extent(r).width)
#     max_bar_height = max(bar_heights)
#     # print(max_bar_height)
            

# 	# ------------------------------- crop -------------------------
#     if max_bar_height < 512:
#         bg = Image.new("RGB", (512, 512), color_bg)
#     else:
#         print('max_bar_height > 512')
#     draw = ImageDraw.Draw(bg)
#     shape = [(512/2-bar_width/2, 512/2-max_bar_height/2), (512/2+bar_width/2, 512/2+max_bar_height/2)] # lefttop_xy, rightbottom_xy
#     draw.rectangle(shape, fill='white')
#     bg.save('output/mask/bar/mask_highest.png')
#     plt.style.use('default')

#     return bar_heights

