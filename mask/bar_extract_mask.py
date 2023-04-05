import sys
import cv2
from PIL import Image
import numpy as np
import os
current_path = os.getcwd()
from extract_color import get_image_colors, draw_colorbar
from bg_removal import bg_removal

def create_mask(img_path, colors):
	with Image.open(img_path).convert('RGB') as im:
		im_array = np.array(im)
		height, width, channels = im_array.shape
		# if channels != 4:
		# 	im = im.convert('RGBA')
		# 	im_array = np.array(im)

		mask_array = np.zeros((height, width), dtype=np.uint8)
		for i, color in enumerate(colors):
			mask_array = np.logical_or(mask_array, np.all(im_array == color, axis=-1))

		mask = Image.fromarray(mask_array.astype(np.uint8)*255) 
		mask.save('output/mask/bar/mask.png')
	return mask


def single_center_mask(mask):
	img = np.array(mask)
	# =================== adjust mask in cetral image ===============
	hh, ww = img.shape

	# ----------------------- detect contour ------------------------
	## input is binary image
	## cv2.RETR_TREE ===> all contour
	## cv2.RETR_EXTERNAL  ===> only external contour
	contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# draw contour
	# img = cv2.drawContours(img, contours, -1, (0,255,0), 3, lineType = cv2.LINE_AA)

	# -------------------- get length of each column  ---------------
	h_highest = 0
	for cntr in contours:
		x,y,w,h = cv2.boundingRect(cntr)
		if h > h_highest:   # find the highest bar
			x_gen, y_gen, w_gen, h_grid = x,y,w,h
			h_highest = h

	# ---------------------------- recenter -------------------------
	startx = (ww - w_gen)//2
	starty = (hh - h_grid)//2
	center_img = np.zeros_like(img)
	center_img[starty:starty+h_grid,startx:startx+w_gen] = img[y_gen:y_gen+h_grid,x_gen:x_gen+w_gen]

	# ------------------------------- crop -------------------------
	new_width = 512 if w_gen < 400 else w_gen*2
	new_height = 512 if w_gen < 400 else int(w_gen*1.3)
	crop_center_x = int((ww - new_width) / 2)
	crop_center_y = int((hh - new_height) / 2)
	# Crop the image using the (left, upper, right, lower) coordinates
	crop_img = np.zeros_like((new_width, new_height))
	crop_img = center_img[crop_center_y:crop_center_y + new_height,crop_center_x:crop_center_x + new_width]

	# save reentered image
	cv2.imwrite('output/mask/bar_highest_mask.png', crop_img)


# test: removel --- color --- mask
image_path = os.path.join(current_path, 'data', 'barchart_83.png')
img = Image.open(image_path)
img_removal = bg_removal(img)
print('--------removel ok---------')

color_list, count_list = get_image_colors(img_removal, scale=0.01)
# print(color_list, count_list)
print('--------color ok---------')

mask = create_mask(image_path, color_list)
print('--------mask ok---------')

single_center_mask(mask)
print('--------single and center ok---------')