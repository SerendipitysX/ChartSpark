from grid.get_grid import *
from PIL import Image, ImageOps, ImageChops
# from get_grid import *
# from PIL import Image, ImageOps, ImageChops
# import os
# current_path = os.getcwd()
# print(current_path)
# module_path = os.path.abspath(os.path.join('mask'))
# if module_path not in sys.path:
#     sys.path.append(module_path)
# from bg_removal import bg_removal

def grid_compile(grid_img_list, sort_idx_array, h, h_highest, h_grid, w):
    margin_h = h_highest - h
    cut_grid_num = margin_h // h_grid
    # print('magin_h:', margin_h)
    # print(cut_grid_num)
    # get origin grid order 1-N
    origin_grid_order = np.arange(0, split_num)
    # new cavas
    new_bar = PIL.Image.new('RGBA', size=(w, h))
    if cut_grid_num == 0: # 还是以前的grid顺序和个数，没有改变
        target_grid_order = origin_grid_order
        h_crop = h_grid - margin_h
        h_sum = 0
        for i, img in enumerate(grid_img_list):
            if i == sort_idx_array[0]: # the meta grid idx
                img = img.crop((0, 0, w, h_crop))
                img.save('output/grid/crop.png')
                new_bar.paste(img, box=(0, h_sum))
                h_sum += h_crop
            else:
                new_bar.paste(img, box=(0, h_sum))
                # new_bar.save('output/grid/new_bar'+str(i)+'.png')
                h_sum += h_grid
    else:
        cut_grid_order = sort_idx_array[:cut_grid_num] # list
        # print('cut_grid_order:', cut_grid_order)
        h_crop = h - (split_num - cut_grid_num - 1)*h_grid
        # print('h_crop:', h_crop)
        if len(cut_grid_order) < split_num and h_crop != 0:
            crop_grid_order = sort_idx_array[cut_grid_num]
        target_grid_order = [i for i in origin_grid_order if i not in cut_grid_order]
        # print(target_grid_order) [0,3,4]
        h_sum = 0
        for i, img in enumerate(grid_img_list):
            if i not in target_grid_order:
                continue
            if i == crop_grid_order: # the crop grid idx
                img = img.crop((0, 0, w, h_crop))
                img.save('output/grid/crop.png')
                new_bar.paste(img, box=(0, h_sum))
                h_sum += h_crop
            else:
                new_bar.paste(img, box=(0, h_sum))
                # new_bar.save('output/new_bar'+str(i)+'.png')
                h_sum += h_grid
    return new_bar # PIL

# split_num = 5
# # get from mask part
# h_list = [131, 106, 212, 400]
# # h_highest = 134
# w = 34
# w_list = [34,34,34,34]

# print(current_path)
# image_path = os.path.join(current_path, 'carrot.jpg')
# print(image_path)
# # bg removal
# lucky = Image.open("carrot.jpg").convert("RGB").resize((512,512))
# img_removal = bg_removal(lucky, current_path)
# # get box of correct object and get the total_h(h_total)
# img_removal_correct, h_total, (h_highest, w, channel) = get_box_img(img_removal)
# print(h_highest)
# # cut
# grid_dict, h_grid = get_grid(img_removal_correct, h_total)
# # get similarity matrix
# sim_matrix = np.ones((split_num, split_num))
# sort_idx_array, sim_mean = ssim_matrix_compute(grid_dict, sim_matrix)
# # show all grid and meta_grid
# grid_meta, grid_img_list = get_grid_meta(grid_dict, sort_idx_array)
   
# ## compile grids again 
# print('the h_grid is:', h_grid)
# for i, h in enumerate(h_list):
#     if h != h_highest:
#         print(h)
#         new_bar = grid_compile(grid_img_list, sort_idx_array, h, h_highest, h_grid)
#         new_bar.save('output/grid/new_bar' + str(i) + '.png')

