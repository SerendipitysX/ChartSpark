import sys
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import math
import json
from PIL import Image, ImageDraw, ImageOps, ImagePath
current_path = os.getcwd()
# import matplotlib as mpl
color_bg = "black"

def table2img_bar(x, y, aspect_ratio, title, y_limit=None, bar_width=0.8):
    plt.rcParams['svg.fonttype'] = 'none'
    plt.rcParams['text.usetex'] = 'False'
    fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
    if isinstance(x[0], str): # x is words
        labels = np.arange(len(x))
        ax.bar(labels, y, width=bar_width, color="skyblue")
        ax.set_xticks(labels)
        ax.set_xticklabels(x)
    else: # x is words
        ax.bar(x, y, width=bar_width, color="skyblue")
        ax.set_xticks(x)
        ax.set_xticklabels(x)
    ax.set_title(title)
    if y_limit != None:
        ax.set_ylim(y_limit)
    # ax.axis('off')
    # ax.set_xlabel("age group")
    # ax.set_ylabel("time hours")
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    fig.savefig('output/preview/bar_preview.png', dpi=fig.dpi)
    fig.savefig('C:/Users/user/A-project/speak/frontend/src/assets/preview/bar_preview.png', dpi=fig.dpi)
    ### save SVG
    # mpl.use("svg")
    # new_rc_params = {'text.usetex': False,
    # "svg.fonttype": 'none'
    # }
    # mpl.rcParams.update(new_rc_params)
    fig.savefig("C:/Users/user/A-project/speak/frontend/src/assets/preview/plot.svg", transparent = True, format="svg", dpi=fig.dpi)
    # mpl.use("module://matplotlib_inline.backend_inline")
    return 'C:/Users/user/A-project/speak/frontend/src/assets/preview/bar_preview.png'

def img2mask_bar(x, y, aspect_ratio, y_limit=None, bar_width=0.8):
    mask_path_foreground = []
    mask_path_background = []

    # get the mask
    # reverse
    fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
    if isinstance(x[0], str): # x is words
        labels = np.arange(len(x))
        bars = plt.bar(labels, y, width=bar_width, color='black')
    else: # x is words
        bars = plt.bar(x, y, width=bar_width, color='black')
    plt.xticks(labels)
    if y_limit != None:
        ax.set_ylim(y_limit)
    ax.axis('off')
    fig.savefig('output/mask/bar/background/mask_reverse.png', dpi=fig.dpi)
    fig.savefig('frontend/src/assets/mask/bar/background/mask_reverse.png', dpi=fig.dpi)
    mask_path_background.append("src/assets/mask/bar/background/mask_reverse.png")

    # all 
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
    if isinstance(x[0], str): # x is words
        labels = np.arange(len(x))
        bars = plt.bar(labels, y, width=bar_width, color='white')
    else: # x is words
        bars = plt.bar(x, y, width=bar_width, color='white')
    if y_limit != None:
        ax.set_ylim(y_limit)
    ax.axis('off')
    fig.savefig('output/mask/bar/foreground/mask_all.png', dpi=fig.dpi)
    fig.savefig('frontend/src/assets/mask/bar/foreground/mask_all.png', dpi=fig.dpi)
    mask_path_foreground.append("src/assets/mask/bar/foreground/mask_all.png")

    # get the mask
    # single
    ww, hh = fig.canvas.get_width_height()
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    bar_heights = [int(bar.get_window_extent(r).height) for bar in bars]
    bar_width = int(bars[0].get_window_extent(r).width)
    max_bar_height = max(bar_heights)
    with open("output/mask/bar/bar_heights.json", "w") as f:
        json.dump(bar_heights, f)

	# ------------------------------- crop -------------------------
    if max_bar_height < 512:
        bg = Image.new("RGB", (512, 512), color_bg)
    else:
        print('max_bar_height > 512')
        print(ww, hh)
    i = 0
    for bar_h in bar_heights:
        bg = Image.new("RGB", (512, 512), color_bg)
        draw = ImageDraw.Draw(bg)
        shape = [(512/2-bar_width/2, 512/2-bar_h/2), (512/2+bar_width/2, 512/2+bar_h/2)] # lefttop_xy, rightbottom_xy
        draw.rectangle(shape, fill='white')
        bg.save('output/mask/bar/foreground/mask_' + str(i) + '.png')
        bg.save('frontend/src/assets/mask/bar/foreground/mask_' + str(i) + '.png')
        mask_path_foreground.append('src/assets/mask/bar/foreground/mask_' + str(i) + '.png')
        i += 1

    if max_bar_height < 512:
        bg = Image.new("RGB", (512, 512), color_bg)
    else:
        print('max_bar_height > 512')
    draw = ImageDraw.Draw(bg)
    shape = [(512/2-bar_width/2, 512/2-max_bar_height/2), (512/2+bar_width/2, 512/2+max_bar_height/2)] # lefttop_xy, rightbottom_xy
    draw.rectangle(shape, fill='white')
    bg.save('output/mask/bar/mask_highest.png')
    # bg.save('output/mask/bar/mask_highest.png')
    plt.style.use('default')

    return bar_heights, mask_path_foreground, mask_path_background


