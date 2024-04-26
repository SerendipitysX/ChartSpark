import sys
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import math
from PIL import Image, ImageDraw, ImageOps, ImagePath
current_path = os.getcwd()
# color_bg = "#7d7d7d"
color_bg = "black"

def table2img_line(x, y, aspect_ratio, title, y_limit, four_corners):
    plt.rcParams['svg.fonttype'] = 'none'
    plt.rcParams['text.usetex'] = 'False'
    fig, ax = plt.subplots(figsize=aspect_ratio, dpi=96) # pixel size=(dpi*w, dpi*h)
    # points, = ax.plot(x, y, marker='o', markerfacecolor='blue', markersize=8, color='skyblue', linewidth=2)
    points, = ax.plot(x, y, color='skyblue', linewidth=3)
    if y_limit != None:
        ax.set_ylim(y_limit)
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    four_corners = [x_min, x_max, y_min, y_max]

    # if four_corners==None:
    #     ax.axis([min(x)-1, max(x)+1, min(y)-1, max(y)+1])
    #     four_corners = [min(x)-1, max(x)+1, min(y)-1, max(y)+1]
    # else:
    #     ax.axis([four_corners[0], four_corners[1], four_corners[2], four_corners[3]])


    # Get the x and y data and transform it into pixel coordinates
    
    if type(x[0]) != str :
        xy_pixels = ax.transData.transform(np.vstack([x,y]).T)
    else:
        xy_pixels = ax.transData.transform(np.vstack([list(range(len(x))),y]).T)
    xpix, ypix = xy_pixels.T
    # get the 4 corners' coordinates (lt-lb-rb-rt)
    x_corners = [four_corners[0], four_corners[0], four_corners[1], four_corners[1]]
    y_corners = [four_corners[3], four_corners[2], four_corners[2], four_corners[3]]
    xy_corners_pixels = ax.transData.transform(np.vstack([x_corners, y_corners]).T)
    x_corner_pix, y_corner_pix = xy_corners_pixels.T


    # # In matplotlib, (0,0) is the left-bottom corner
    # # In pillow, (0, 0) is the left-top corner
    width, height = fig.canvas.get_width_height()
    ypix = height - ypix
    xy_pix = np.vstack([xpix,ypix]).T.astype(int)
    # corners
    y_corner_pix = height - y_corner_pix
    xy_corners_pixels = np.vstack([x_corner_pix, y_corner_pix]).T.astype(int)

    ax.set_title(title)
    # ax.axis('off')
    # ax.set_xlabel("Year")
    # ax.set_ylabel("number of cases of accidental fire")
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    fig.savefig('output/preview/line_preview.png', dpi=fig.dpi)
    fig.savefig('C:/Users/user/A-project/speak/frontend/src/assets/preview/line_preview.png', dpi=fig.dpi)
    fig.savefig("C:/Users/user/A-project/speak/frontend/src/assets/preview/plot.svg", transparent = True, format="svg", dpi=fig.dpi)
    return 'output/preview/line_preview.png', xy_pix, (width, height), xy_corners_pixels


def img2mask_line(pos_pix, fig_size, xy_corners_pix, y_limit):
    mask_path_foreground = []
    mask_path_background = []

    # creating new Image object
    bg = Image.new("RGB", fig_size, color_bg)
    draw = ImageDraw.Draw(bg)

    # create line image
    for i in range(len(pos_pix)-1):
        draw.line([tuple(pos_pix[i]), tuple(pos_pix[i+1])], fill ="white", width = 10)    
    bg.save('output/mask/line/foreground/mask1.png')
    bg.save('C:/Users/user/A-project/speak/frontend/src/assets/mask/line/foreground/mask1.png')
    mask_path_foreground.append("src/assets/mask/line/foreground/mask1.png")
    bg_reverse = ImageOps.invert(bg)
    bg_reverse.save('output/mask/line/background/mask2.png')
    bg_reverse.save('C:/Users/user/A-project/speak/frontend/src/assets/mask/line/background/mask2.png')
    mask_path_background.append("src/assets/mask/line/background/mask2.png")

    # create shape mask --1
    # path = [(pos_pix[0][0], fig_size[1])] + [tuple(pos) for pos in pos_pix] + [(pos_pix[-1][0], fig_size[1])]
    # bg = Image.new("RGB", fig_size, color_bg)
    # draw = ImageDraw.Draw(bg)
    # draw.polygon(path, fill='white')
    # bg.save('output/mask/line/mask3.png')
    # bg_reverse = ImageOps.invert(bg)
    # bg_reverse.save('output/mask/line/mask4.png')
    # path = [(pos_pix[0][0], 0)] + [tuple(pos) for pos in pos_pix] + [(pos_pix[-1][0], 0)]
    # bg = Image.new("RGB", fig_size, color_bg)
    # draw = ImageDraw.Draw(bg)
    # draw.polygon(path, fill='white')
    # bg.save('output/mask/line/mask5.png')
    # bg_reverse = ImageOps.invert(bg)
    # bg_reverse.save('output/mask/line/mask6.png')

    # create shape mask --2
    # top
    y_array = np.array(pos_pix)[:,1]
    max_idx_y = np.argmax(y_array)
    if max_idx_y != len(pos_pix) or max_idx_y != 0:
        path = [tuple(xy_corners_pix[0])] + [tuple(pos) for pos in pos_pix] + [tuple(xy_corners_pix[3])]
    else:
        path = [tuple((pos_pix[0][0], pos_pix[-1][1]))] + [tuple(pos) for pos in pos_pix]# + [tuple(xy_corners_pix[3])]
    bg = Image.new("RGB", fig_size, color_bg)
    draw = ImageDraw.Draw(bg)
    draw.polygon(path, fill='white')
    bg.save('output/mask/line/foreground/mask7.png')
    bg.save('frontend/src/assets/mask/line/foreground/mask7.png')
    mask_path_foreground.append("src/assets/mask/line/foreground/mask7.png")
    bg_reverse = ImageOps.invert(bg)
    bg_reverse.save('output/mask/line/background/mask8.png')
    bg_reverse.save('frontend/src/assets/mask/line/background/mask8.png')
    mask_path_background.append("src/assets/mask/line/background/mask8.png")

    # bottom
    if max_idx_y != len(pos_pix) or max_idx_y != 0:
        path = [tuple(xy_corners_pix[1])] + [tuple(pos) for pos in pos_pix] + [tuple(xy_corners_pix[2])]
    else:
        path = [tuple((pos_pix[-1][0], pos_pix[0][1]))] + [tuple(pos) for pos in pos_pix]# + [tuple(xy_corners_pix[2])]
    bg = Image.new("RGB", fig_size, color_bg)
    draw = ImageDraw.Draw(bg)
    draw.polygon(path, fill='white')
    bg.save('output/mask/line/foreground/mask9.png')
    bg.save('frontend/src/assets/mask/line/foreground/mask9.png')
    mask_path_foreground.append("src/assets/mask/line/foreground/mask9.png")
    bg_reverse = ImageOps.invert(bg)
    bg_reverse.save('output/mask/line/background/mask10.png')
    bg_reverse.save('frontend/src/assets/mask/line/background/mask10.png')
    mask_path_background.append("src/assets/mask/line/background/mask10.png")

    return mask_path_foreground, mask_path_background


# #===================== from table ======================
# # user defined data
# a = {"x": [2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020], "y": [150, 155, 140, 133, 170, 148, 157, 152], "title": "Date of cherry blossom in High Park"} 
# a = {"x": [2003, 2005, 2007, 2009, 2011, 2013], "y": [19956, 20106, 21839, 24884, 26343, 23593], "title": "Number of Cases of Accidental Fire in India"}
# # a = {"x": ["15 to 19 years", "25 to 34 years", "45 to 54 years", "65 to 74 years"], "y": [0.16, 0.13, 0.26, 0.49], "title": "Average daily time spent reading per capita in US in 2021"}
# x = a["x"]
# y = a["y"]
# title = a["title"] 
# aspect_ratio = (8, 6)
# y_limit = None

# # table to img_preview
# _, pos_pix, fig_size, xy_corners_pix = table2img_line(x, y, aspect_ratio, title, y_limit, four_corners = None)
# img2mask_line(pos_pix, fig_size, xy_corners_pix, y_limit)
