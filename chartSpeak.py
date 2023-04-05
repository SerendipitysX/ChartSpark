from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from mask.bar_mask import *
from mask.line_mask import *
from mask.pie_mask import *
from mask.scatter_mask import *
from theme_extract.similar_text import extract_kw_similar
from theme_extract.theme_wc import WordCloudGenerator
import warnings
import random
import torch
import requests
from PIL import Image, ImageOps
import PIL
from io import BytesIO
import base64
from diffusers import StableDiffusionDepth2ImgPipeline,StableDiffusionImg2ImgPipeline,StableDiffusionPipeline
from generation.FE import text2img_element, extract_element
from generation.FIS import FIS_bar, FIS_line, FIS_pie
from generation.BG import BG_bar, BG_line, BG_pie, BG_scatter
warnings.filterwarnings("ignore")

# torch.manual_seed(0)
model_id = "runwayml/stable-diffusion-v1-5"
model_depth = "stabilityai/stable-diffusion-2-depth"
# pipe_text2img = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")
# pipe_depth = StableDiffusionDepth2ImgPipeline.from_pretrained(model_depth,torch_dtype=torch.float16).to("cuda")
# pipe_img2img = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")

figure_size = None

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

def pil_to_data_uri(pil_img):
    # Convert PIL image to bytes
    img_bytes = BytesIO()
    pil_img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()

    # Encode bytes as base64 string
    img_base64 = base64.b64encode(img_bytes).decode()

    # Create data URI
    data_uri = 'data:image/jpeg;base64,' + img_base64

    # Create HTML string with image tag
    html_str = f'<img src="{data_uri}">'

    return html_str

@app.route('/setting1',methods=['GET', 'POST'])
def setting_preview_wc():
    print(request.get_json())
    data = request.get_json()
    chart_type = data["chart-type"]
    aspect_ratio = data["aspect-ratio"]
    bar_width = data["bar_width"]
    chart_data = data["data"]
    try:
        y_min = data["y_min"]
        y_max = data["y_max"]
    except:
        pass
    chart_json = json.loads(chart_data)

    # get shuju
    x = chart_json["x"]
    y = chart_json["y"]
    title = chart_json["title"]
    if chart_type == "scatter":
        # z = chart_json["z"]
        z = []

    # user defined data
    aspect_ratio_fronend = ['1:1', '3:2', '4:3', '5:4']
    ratio_id = aspect_ratio_fronend.index(aspect_ratio)
    aspect_ratio = [(5,5), (5.5,3.7), (4, 3), (5, 4)]
    global figure_size
    figure_size = aspect_ratio[ratio_id]
    print("====================================")
    print(figure_size)
    if "y_min" in locals() and "y_max" in locals():
        # 使用 y_min 变量
        print(y_min, y_max)
        y_limit = (y_min, y_max)
    else:
        y_limit = None # (-3, 50)

    if chart_type=="bar":
        img_path1 = table2img_bar(y, x, aspect_ratio[ratio_id], title, y_limit, bar_width)
        img2mask_bar(y, x, aspect_ratio[ratio_id], y_limit)
    if chart_type == "line":
        img_path1, pos_pix, fig_size, xy_corners_pix = table2img_line(x, y, aspect_ratio[ratio_id], title, y_limit, four_corners = None)
        img2mask_line(pos_pix, fig_size, xy_corners_pix, y_limit)
    if chart_type == "pie":
        img_path1 = table2img_pie(y, x, aspect_ratio[ratio_id], title)
        img2mask_pie(y, x, aspect_ratio[ratio_id])
    if chart_type == "scatter":
        img_path1 = table2img_scatter(x, y, z, title, y_limit, aspect_ratio[ratio_id])
        img2mask_scatter(x, y, z, y_limit, aspect_ratio[ratio_id])
    d = extract_kw_similar(title)
    wordcloud_gen = WordCloudGenerator(font_path='D:/speak/frontend/src/assets/fonts/TiltNeon-Regular.ttf',  
                                    background_color='#F5F5F5', colormap="binary",  
                                    prefer_horizontal=1, 
                                    max_font_size=45, min_font_size=12, 
                                    width=420, height=200, 
                                    margin=50, d=d)
    img_path2 = wordcloud_gen.generate_wordcloud()
    return [img_path1, img_path2]

@app.route('/generate_element',methods=['GET', 'POST'])
def generate_element():
    data = request.get_json()
    num_to_generate = data["num_to_generate"]
    method_to_generate = data["method_to_generate"]
    object_info = data["object"]
    description = data["description"]
    chart_bool_list = data["chart_type"]
    guide = data["guide"]
    print(method_to_generate, guide)
    print(chart_bool_list)
    # object_info = "A single bluberry"
    # description = "close up"
    prompt = object_info + ", " + description
    chart_type_list = ["bar", "line", "pie", "scatter"]
    chart_type = chart_type_list[chart_bool_list.index(True)]

    # global figure_size
    # if figure_size[0] < 10:
    #     figure_size = tuple([int(i * 96) for i in figure_size])
    # print(figure_size)
    # figure_size = (512, 512)

    img_list = []
    # if method_to_generate == "FE" and guide == "UNC":
    #     for i in range(num_to_generate):
    #         img_text2img = text2img_element(pipe_text2img, prompt)
    #         img_list.append(extract_element(img_text2img))

    # if method_to_generate == "FE" and guide == "C":
    #     if chart_type == "bar":
    #         folder = os.getcwd()
    #         img_pth = os.path.join(folder, 'output\mask\/bar\mask_highest.png')
    #         bar_mask = PIL.Image.open(img_pth).convert('RGB')#.resize((512,512))
    #         img_list = FIS_bar(prompt, bar_mask, num_to_generate, figure_size, pipe_text2img, pipe_img2img, pipe_depth)
    #     if chart_type == "line":
    #         folder = os.getcwd()
    #         # which mask??????????????????????
    #         img_pth = os.path.join(folder, 'output\mask\line\mask1.png')
    #         line_mask = PIL.Image.open(img_pth).convert('RGB')#.resize((512,512))
    #         img_list = FIS_line(prompt, line_mask, num_to_generate, figure_size, pipe_text2img, pipe_img2img, pipe_depth)
    #     if chart_type == "pie":
    #         folder = os.getcwd()
    #         line_mask = PIL.Image.open(img_pth).convert('RGB')#.resize((512,512))
    #         img_list = FIS_pie(prompt, line_mask, num_to_generate, figure_size, pipe_text2img, pipe_img2img, pipe_depth)
    #     if chart_type == "scatter":
    #         for i in range(num_to_generate):
    #             img_text2img = text2img_element(pipe_text2img, prompt)
    #             img_list.append(extract_element(img_text2img))

    # if method_to_generate == "B" and guide == "UNC":
    #     for i in range(num_to_generate):
    #         img_text2img = pipe_text2img(prompt=prompt, width=figure_size[0], height=figure_size[1], guidance_scale=7.5).images[0]
    #         img_list.append(extract_element(img_text2img))

    # if method_to_generate == "B" and guide == "C":
    #     if chart_type == "bar":
    #         folder = os.getcwd()
    #         img_pth = os.path.join(folder, 'output\mask\/bar\mask_highest.png')
    #         bar_mask = PIL.Image.open(img_pth).convert('RGB')#.resize((512,512))
    #         img_list = FIS_bar(prompt, bar_mask, num_to_generate, figure_size, pipe_text2img, pipe_img2img, pipe_depth)
    #     if chart_type == "line":
    #         folder = os.getcwd()
    #         img_pth = os.path.join(folder, 'output\mask\line\mask1.png')
    #         line_mask = PIL.Image.open(img_pth).convert('RGB')#.resize((512,512))
    #         img_list = FIS_line(prompt, line_mask, num_to_generate, figure_size, pipe_text2img, pipe_img2img, pipe_depth)
    #     if chart_type == "pie":
    #         folder = os.getcwd()
    #         line_mask = PIL.Image.open(img_pth).convert('RGB')#.resize((512,512))
    #         img_list = FIS_pie(prompt, line_mask, num_to_generate, figure_size, pipe_text2img, pipe_img2img, pipe_depth)
    #     if chart_type == "scatter":
    #         for i in range(num_to_generate):
    #             img_text2img = text2img_element(pipe_text2img, prompt)
    #             img_list.append(extract_element(img_text2img))
    
    # if type(img_list[0])!=str:
    #     html_img_list = [pil_to_data_uri(img) for img in img_list]
    #     return html_img_list
    # else:
    #     return img_list
    
    # SAKURA
    img_dir = "/src/assets/generation/"
    if method_to_generate == "F" and guide == "UNC":
        print(111111111111111111)
        if num_to_generate == 4:
            img_list = [img_dir+"flower/1.jpg", img_dir+"flower/2.jpg", img_dir+"flower/4.jpg", img_dir+"flower/6.jpg"]
        else:
            img_list = [img_dir+"flower/5.jpg"]
    if method_to_generate == "F" and guide == "C":
        if num_to_generate == 4:
            img_list = [img_dir+"branch/branch5.jpg", img_dir+"branch/7.jpg", img_dir+"branch/8.jpg", img_dir+"branch/branch4.png"]
        else:
            img_list = [img_dir+"branch/branch.png"]
    if method_to_generate == "B" and guide == "UNC":
        if num_to_generate == 4:
            img_list = [img_dir+"bg/bg14.png", img_dir+"bg/bg11.png", img_dir+"bg/bg12.png", img_dir+"bg/bg13.png"]
    return img_list
    

    # img_list = []
    # img_dir = "/src/assets/generation/"
    # for i in range(10):
    #     img_path = img_dir + str(i) + ".png"
    #     img_list.append(img_path)
    # items = random.sample(img_list, num_to_generate)
    # return items

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=88, debug=True)

