import sys
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import math
from PIL import Image, ImageDraw, ImageOps, ImagePath
current_path = os.getcwd()


def table2img_pie(sizes, labels, aspect_ratio, title):
    plt.rcParams['svg.fonttype'] = 'none'
    plt.rcParams['text.usetex'] = 'False'
    colors_list = ['skyblue', '#B7C3F3', '#F5E9CF', '#DD7596', '#8EB897', '#FEC868', '#4F6272', '#AA5656']
    fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
    # ax.pie(sizes, labels=labels, labeldistance=1.15,  
    # wedgeprops = {'linewidth' : 2, 'edgecolor' : 'white'}, colors=colors_list[:len(sizes)])
    ax.pie(sizes, labels=labels, labeldistance=1.15,  
    wedgeprops = {'linewidth' : 2, 'edgecolor' : 'white'}, colors=colors_list[:len(sizes)])
    
    ax.set_title(title)   
    # DEFAULT: start_angle = 0, counterclockwise
    ax.axis('off')
    fig.savefig('output/preview/pie_preview.png', dpi=fig.dpi)
    fig.savefig('frontend/src/assets/preview/pie_preview.png', dpi=fig.dpi)
    fig.savefig("frontend/src/assets/preview/plot.svg", transparent = True, format="svg", dpi=fig.dpi)
    return 'frontend/src/assets/preview/pie_preview.png'



def img2mask_pie(sizes, labels, aspect_ratio):
    mask_path_foreground = []
    mask_path_background = []
    # get the mask
    # all
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
    colors_mask_list = ['white' for _ in range(len(sizes))]
    ax.pie(sizes, labeldistance=1.15,
    wedgeprops = {'linewidth' : 0, 'edgecolor' : 'black'}, colors=colors_mask_list)
    fig.savefig('output/mask/pie/foreground/mask_all.png', dpi=fig.dpi)
    fig.savefig('frontend/src/assets/mask/pie/foreground/mask_all.png', dpi=fig.dpi)
    mask_path_foreground.append("src/assets/mask/pie/foreground/mask_all.png")

    # a circle
    fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
    colors_mask_list = ['white']
    ax.pie([1], wedgeprops = {'linewidth' : 2, 'edgecolor' : 'black'}, colors=colors_mask_list)
    fig.savefig('output/mask/pie/mask_circle.png', dpi=fig.dpi)

    # single
    fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
    colors_mask_list = ['black' for _ in range(len(sizes))]
    for i in range(len(sizes)):
        tmp = colors_mask_list.copy()
        tmp[i] = 'white'
        ax.pie(sizes, labeldistance=1.15,
        wedgeprops = {'linewidth' : 2, 'edgecolor' : 'black'}, colors=tmp)
        fig.savefig('output/mask/pie/foreground/mask_'+ str(i) +'.png', dpi=fig.dpi)
        fig.savefig('frontend/src/assets/mask/pie/foreground/mask_'+ str(i) +'.png', dpi=fig.dpi)
        mask_path_foreground.append('src/assets/mask/pie/foreground/mask_'+ str(i) +'.png')

    plt.style.use('default')
    fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96)
    colors_mask_list = ['black' for _ in range(len(sizes))]
    ax.pie(sizes, labeldistance=1.15,
    wedgeprops = {'linewidth' : 2, 'edgecolor' : 'white'}, colors=colors_mask_list)
    fig.savefig('output/mask/pie/background/mask_reverse.png', dpi=fig.dpi)
    fig.savefig('frontend/src/assets/mask/pie/background/mask_reverse.png', dpi=fig.dpi)
    mask_path_background.append('src/assets/mask/pie/background/mask_reverse.png')
    return mask_path_foreground, mask_path_background


# # user defined data
# # a = {"x": ["farmland", "desert", "forest"], "y": [25, 65, 55], "title": "Area of the Kubuqi Desert and the Restoration in 2001"}
# a = {"x": ["green veggies", "citrus fruits", "sweet fruits and veggies"], "y": [0.1, 0.15, 0.75], "title": "A recipe for healthy juice composition"}
# labels = a["x"]
# sizes = a["y"]
# title = a["title"]
# # explode_item_list = ['Frogs', 'Dogs']
# aspect_ratio = (8, 6)
# # explde setting in backend
# # explode_list = [0]*len(sizes)
# # if explode_item_list!=None:
# #     for item in explode_item_list:
# #         explode_list[labels.index(item)] = 0.1

# table2img_pie(sizes, labels, aspect_ratio, title)
# img2mask_pie(sizes, labels, aspect_ratio)