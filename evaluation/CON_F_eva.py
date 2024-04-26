import pandas as pd
import numpy as np
import cv2
import os
import sys
from PIL import Image, ImageDraw, ImageOps
from scipy.spatial import distance


class BarEvaluation:
    def __init__(self):
        pass

    def init_gray(self, to_be_evaluate):
        rect_image = Image.new("RGBA", to_be_evaluate.size)

        draw = ImageDraw.Draw(rect_image)

        draw.rectangle([(0, 0), (to_be_evaluate.size[0], to_be_evaluate.size[1])], fill=(218, 218, 218, 250))

        result = Image.alpha_composite(to_be_evaluate, rect_image)
        img_arr = np.array(result)
        to_be_evaluate_arr = np.array(to_be_evaluate)
        img_arr[to_be_evaluate_arr[:,:,3]==0] = [0,0,0,0]
        result = Image.fromarray(img_arr)
        return result

    def higher_draw(self, to_be_evaluate, x, y, w, h):
        rect_image = Image.new("RGBA", to_be_evaluate.size)

        draw = ImageDraw.Draw(rect_image)

        draw.rectangle([(x, y), (x + w, y + h)], fill=(255, 0, 0, 200))

        result = Image.alpha_composite(to_be_evaluate, rect_image)
        img_arr = np.array(result)
        to_be_evaluate_arr = np.array(to_be_evaluate)
        img_arr[to_be_evaluate_arr[:,:,3]==0] = [0,0,0,0]
        result = Image.fromarray(img_arr)
        return result

    def lower_draw(self, to_be_evaluate, x, y, w, h, h_mask, h_max):
        draw = ImageDraw.Draw(to_be_evaluate)
        draw.line([(x, h_max-h), (x, h_max-h_mask)], fill='red')
        draw.line([(x, h_max-h_mask), (x+w, h_max-h_mask)], fill='red')
        draw.line([(x+w, h_max-h_mask), (x+w, h_max-h)], fill='red')
        return to_be_evaluate

    def get_h_list(self, input_image, evaluate=False):
        img_arr = np.array(input_image)
        if img_arr.shape[2]==4:
            img_arr[img_arr[:,:,3]==0] = [0,0,0,0]
        imgray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 0, 255, 0)
        cv2.imwrite('output/grid/thresh.png', thresh)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        x_list, y_list, w_list, h_list = [], [], [], []
        for cntr in contours:
            x,y,w,h = cv2.boundingRect(cntr)
            x_list.append(x)
            y_list.append(y)
            w_list.append(w)
            h_list.append(h)
        if evaluate == True:
            # cv2.drawContours(img_arr,contours,-1,(0,0,255,175),2)
            image = Image.fromarray(img_arr)
            return image, x_list, y_list, w_list, h_list
        else:
            return x_list, y_list, w_list, h_list
        
    def get_score_all_F(self, h_list_eval, h_list):
        a = np.array([h_list_eval, h_list])
        score_eval = round((1-np.mean(np.abs(a[0,:]-a[1,:])/a[1,:]))*100, 1)
        if max(h_list_eval) - max(h_list) < 0:
            extend_size = True
        else:
            extend_size = False
        return score_eval, extend_size

    def __call__(self, mask_path, mask_single_FLAG, count):
        to_be_evaluate = Image.open("output/to_be_evaluate.png").convert("RGBA")
        to_be_evaluate = self.init_gray(to_be_evaluate)
        w_max, h_max = to_be_evaluate.size
        mask_pil = Image.open(mask_path)
        image, x_list_eval, y_list_eval, w_list_eval, h_list_eval = self.get_h_list(to_be_evaluate, evaluate=True)
        _, _, _, h_list = self.get_h_list(mask_pil)
        if mask_single_FLAG == True:
            score_eval, extend_size = self.get_score_all_F([h_max], h_list)
            if extend_size: 
                print("The original one is higher than the generated bar!")
                new_bg = Image.new("RGBA", (w_max+5, max(h_list)))
                new_bg.paste(to_be_evaluate, (0, max(h_list)-max(h_list_eval)))
                to_be_evaluate = new_bg
                image = self.lower_draw(to_be_evaluate, 0, _, w_max, h_max, h_list[0], h_list[0])
            else:
                print("The generated bar is higher than the original one!")
                image = self.higher_draw(to_be_evaluate, 0, 0, w_max, np.abs(h_list[0]-h_max))
        if mask_single_FLAG == False:
            print(h_list_eval, h_list)
            score_eval, extend_size = self.get_score_all_F(h_list_eval, h_list)
            if extend_size:
                new_bg = Image.new("RGBA", (w_max+5, max(h_list)))
                new_bg.paste(to_be_evaluate, (0, max(h_list)-max(h_list_eval)))
                to_be_evaluate = new_bg
                w_max, h_max = to_be_evaluate.size
                image, x_list_eval, y_list_eval, w_list_eval, h_list_eval = self.get_h_list(to_be_evaluate, evaluate=True)
            for i in range(len(h_list)):
                if h_list_eval[i] > h_list[i]:
                    if i == 0:
                        image = self.higher_draw(to_be_evaluate, x_list_eval[i], y_list_eval[i], w_list_eval[i], np.abs(h_list[i]-h_list_eval[i]))
                    else:
                        image = self.higher_draw(image, x_list_eval[i], y_list_eval[i], w_list_eval[i], np.abs(h_list[i]-h_list_eval[i]))         
                else:
                    if i == 0:
                        image = self.lower_draw(to_be_evaluate, x_list_eval[i], y_list_eval[i], w_list_eval[i], h_list_eval[i], h_list[i], h_max)
                    else:
                        image = self.lower_draw(image, x_list_eval[i], y_list_eval[i], w_list_eval[i], h_list_eval[i], h_list[i], h_max)
        image.save("frontend/src/assets/evaluation/evaluation_"+str(count)+".png")
        result = {"score_eval":score_eval, "eval_img_path":"src/assets/evaluation/evaluation_"+str(count)+".png"}
        return result
    

class LineEvaluation:
    def __init__(self):
        pass

    def extract_axis_from_line(self, image):
        image_r = np.array(image, dtype="uint8")
        if image_r.shape[-1] != 4:
            ret,binary=cv2.threshold(image_r[:,:,2],0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
        else:
            ret,binary=cv2.threshold(image_r[:,:,3],0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
        thin=cv2.ximgproc.thinning(binary)
        contours,hireachy=cv2.findContours(thin,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        white_image = np.ones((image.size[1], image.size[0]), dtype="uint8")*255
        cv2.drawContours(white_image,contours,-1,(21,153,149),2)
        white_image = np.tile(white_image[:,:,np.newaxis], [1,1,3])
        white = Image.fromarray(white_image)
        return white, contours

    def compute_pixel(self, axis_white, contours):
        window_size = 7

        kernel = np.ones((window_size, window_size), dtype=np.float32)/(window_size**2)

        filtered_img = cv2.filter2D(np.array(axis_white), -1, kernel)
        sample_list = []
        pixel_value_list = []
        for i, (x,y) in enumerate(contours[0].squeeze()):
            if i%5==0:
                x_start = x - int(window_size/2)
                y_start = y - int(window_size/2)
                x_end = x_start + window_size
                y_end = y_start + window_size
                region = filtered_img[y_start:y_end, x_start:x_end]
                avg_value = np.mean(region)
                sample_list.append((x,y))
                pixel_value_list.append(avg_value)
        return pixel_value_list, sample_list

    def cal_score(self, pixel_value_list, pixel_value_list_g):        
        score_list = []
        for i in range(min(len(pixel_value_list), len(pixel_value_list_g))):
            s1 = pixel_value_list[i]
            s2 = pixel_value_list_g[i]
            score_list.append(1-np.abs(s1-s2)/255)
        min_score = np.min(score_list)
        max_socre = np.max(score_list)
        score_list1 = [(score-min_score)/(max_socre-min_score) for score in score_list]
        score = sum(score_list1)/len(score_list1)
        return round(score*100, 1), score_list1

    def init_gray(self, to_be_evaluate):
        rect_image = Image.new("RGBA", to_be_evaluate.size)

        draw = ImageDraw.Draw(rect_image)

        draw.rectangle([(0, 0), (to_be_evaluate.size[0], to_be_evaluate.size[1])], fill=(218, 218, 218, 250))

        result = Image.alpha_composite(to_be_evaluate, rect_image)
        img_arr = np.array(result)
        to_be_evaluate_arr = np.array(to_be_evaluate)
        img_arr[to_be_evaluate_arr[:,:,3]==0] = [0,0,0,0]
        result = Image.fromarray(img_arr)
        return result

    def vis_axis(self, image_RGBA, sample_list, score_list1):    
        patch = np.zeros((9, 9, 3), dtype=np.uint8) 
        patch[:, :, :] = (255, 0, 0)
        alpha = np.ones((9, 9), dtype=np.uint8) * 200  
        patch = np.dstack((patch, alpha))  

        img = np.array(self.init_gray(image_RGBA)).copy()
        h, w, _ = np.array(img).shape
        mask = np.ones((h, w), dtype=np.uint8)

        for i in range(len(sample_list)):
            try:
                score = score_list1[i]
                if score < 0.9:
                    x, y = sample_list[i][1], sample_list[i][0]  # 获取指定像素点的坐标
                    x_start, y_start = x - 4, y - 4  # 计算patch的起始坐标
                    x_end, y_end = x + 5, y + 5  # 计算patch的结束坐标
                    img_patch = img[x_start:x_end, y_start:y_end, :]  # 从原图像中抠出patch对应的部分
                    patch_valid = patch[:img_patch.shape[0], :img_patch.shape[1], :]  # 裁剪patch，使其与抠出的部分大小相同
                    mask_valid = mask[x_start:x_end, y_start:y_end]  # 从蒙版中抠出patch对应的部分
                    patched = cv2.addWeighted(img_patch, min(score,0.9), patch_valid, (1-score), 0)  # 在抠出的部分上叠加patch
                    img[x_start:x_end, y_start:y_end, :] = patched  # 将叠加后的patch放回原图像的对应位置
            except:
                pass
        im = Image.fromarray(img)
        return im
    
    def find_distance(self, matrix):
        num_rows = len(matrix)
        num_cols = len(matrix[0])
        distances = []

        for col in range(num_cols):
            first_non_zero = None
            last_non_zero = None

            for row in range(num_rows):
                if matrix[row][col] != 0 and first_non_zero is None:
                    first_non_zero = row
                if matrix[row][col] != 0:
                    last_non_zero = row

            if first_non_zero is None or last_non_zero is None:
                distances.append(0)
            else:
                distance = last_non_zero - first_non_zero
                distances.append(distance)

        return distances
    
    def divide_arrays(self, arr1, arr2):
        result = []
        for i in range(len(arr2)):
            if arr2[i] != 0:
                result.append(arr1[i] / arr2[i])
            else:
                result.append(1)
        aa = (sum(result)/len(result))*100
        print(aa)
        aa = (100/aa)*100-1 if aa>99.9 else aa-0.45
        print(aa)
        print('------------')
        return round(aa, 1)
    
    def __call__(self, mask_path, mask_line_FLAG, count):
        image_RGBA = Image.open("output/to_be_evaluate.png").convert("RGBA")
        mask_pil = Image.open(mask_path).convert("RGB")
        if mask_line_FLAG:
            # extract medal axis
            axis_white_g, contours_g = self.extract_axis_from_line(image_RGBA)
            axis_white, contours = self.extract_axis_from_line(mask_pil)
            # cal pixel
            pixel_value_list_g, _ = self.compute_pixel(axis_white_g, contours_g)
            pixel_value_list, sample_list = self.compute_pixel(axis_white, contours)
            # cal score
            score, score_list = self.cal_score(pixel_value_list, pixel_value_list_g)
            # vis
            im = self.vis_axis(image_RGBA, sample_list, score_list)
        else:
            mask_arr = np.array(mask_pil)[:,:,0]
            img_arr = np.array(image_RGBA)[:,:,3]

            mask_distances = self.find_distance(mask_arr)
            img_distances = self.find_distance(img_arr)

            mask_distances = [x for x in mask_distances if x != 0]
            if len(img_distances)-len(mask_distances)>0:
                mask_distances = [1]*(len(img_distances)-len(mask_distances)) + mask_distances
            if len(mask_distances)-len(img_distances)>0:
                mask_distances = mask_distances[len(mask_distances)-len(img_distances):]
            
            score = self.divide_arrays(img_distances, mask_distances)
            image_array = np.ones((max(mask_distances), len(mask_distances), 3), dtype=np.uint8) * 255
            # bg
            image_array[:, :, :] = 255
            # mask red
            for i, num in enumerate(mask_distances):
                image_array[-num:, i, 0] = 255
                image_array[-num:, i, 1:] = 85
            # image gray
            for i, num in enumerate(img_distances):
                image_array[-num:, i, :] = 218  
            im = Image.fromarray(image_array)

        im.save("frontend/src/assets/evaluation/evaluation_"+str(count)+".png")
        result = {"score_eval":score, "eval_img_path":"src/assets/evaluation/evaluation_"+str(count)+".png"}
        return result
