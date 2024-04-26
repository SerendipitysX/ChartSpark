from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import torch
from utils import clear_folder
from mask.bar_mask import *
from mask.line_mask import *
from mask.pie_mask import *
from mask.scatter_mask import *
from theme_extract.similar_text import extract_kw_similar
from theme_extract.theme_wc import WordCloudGenerator
import warnings
import re
from io import BytesIO
import io
import base64
import random
warnings.filterwarnings("ignore")
current_path = os.getcwd()
print(current_path)
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

# generative model
from diffusers import DiffusionPipeline,StableDiffusionDepth2ImgPipeline,StableDiffusionImg2ImgPipeline,StableDiffusionPipeline
from generation.UNC import text2img, extract_element
from generation.COND_F import LineAssistant, BarAssistant, PieAssistant, ScatterAssistant
from generation.COND_B import LineAssistant_B, BarAssistant_B, PieAssistant_B, ScatterAssistant_B
from evaluation.CON_F_eva import BarEvaluation, LineEvaluation
# from evaluation.CON_B_eva import PieEvaluation
from mask.bg_removal import bg_removal



# ======================= load generative model =======================
model_id = "path/to/models--runwayml--stable-diffusion-v1-5/snapshots/aa9ba505e1973ae5cd05f5aedd345178f52f8e6a"
# e.g. C:/Users/user/.cache/huggingface/hub/models--runwayml--stable-diffusion-v1-5/snapshots/aa9ba505e1973ae5cd05f5aedd345178f52f8e6a
model_depth = "path/to/models--stabilityai--stable-diffusion-2-depth/snapshots/d41a0687231847e8bd55f43fb1f576afaeefef19"
model_paint = "path/to/models--Fantasy-Studio--Paint-by-Example/snapshots/351e6427d8c28a3b24f7c751d43eb4b6735127f7"
pipe_text2img = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16,local_files_only=True).to("cuda")
pipe_depth = StableDiffusionDepth2ImgPipeline.from_pretrained(model_depth,torch_dtype=torch.float16,local_files_only=True).to("cuda")
pipe_img2img = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16,local_files_only=True).to("cuda")
pipe_paint = DiffusionPipeline.from_pretrained(model_paint, torch_dtype=torch.float16,local_files_only=True).to("cuda")
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

def dataurl_to_pil(dataurl, output_path=None):
    # image_data = dataurl.replace("data:image/jpeg;base64,", '')
    image_data = re.sub(r"data:image/\w+;base64,", "", dataurl)
    binary_data = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(binary_data))
    return image

def add_margin(img):
    background = Image.new("RGB", (512, 512), "white")
    x = (background.width - img.width) // 2
    y = (background.height - img.height) // 2
    background.paste(img, (x, y)) # 左上角的坐标
    return background, x, y

@app.route('/setting1',methods=['GET', 'POST'])
def setting_preview_wc():
    clear_folder()
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
        z = chart_json["z"]
        # z = []

    # user defined data
    aspect_ratio_fronend = ['1:1', '3:2', '4:3', '5:4']
    ratio_id = aspect_ratio_fronend.index(aspect_ratio)
    aspect_ratio = [(5,5), (5.5,3.7), (4, 3), (5, 4)]
    global figure_size
    figure_size = aspect_ratio[ratio_id]
    print("====================================")
    print("figure_size: ", figure_size)
    if "y_min" in locals() and "y_max" in locals():
        # 使用 y_min 变量
        print(y_min, y_max)
        y_limit = (y_min, y_max)
    else:
        y_limit = None # (-3, 50)

    print("aspect_ratio[ratio_id]: ", aspect_ratio[ratio_id])
    if chart_type=="bar":
        img_path1 = table2img_bar(x, y, aspect_ratio[ratio_id], title, y_limit, bar_width)
        _, mask_path_foreground, mask_path_background = img2mask_bar(x, y, aspect_ratio[ratio_id], y_limit, bar_width)
    if chart_type == "line":
        img_path1, pos_pix, fig_size, xy_corners_pix = table2img_line(x, y, aspect_ratio[ratio_id], title, y_limit, four_corners = None)
        mask_path_foreground, mask_path_background = img2mask_line(pos_pix, fig_size, xy_corners_pix, y_limit)
    if chart_type == "pie":
        img_path1 = table2img_pie(y, x, aspect_ratio[ratio_id], title)
        mask_path_foreground, mask_path_background = img2mask_pie(y, x, aspect_ratio[ratio_id])
    if chart_type == "scatter":
        img_path1 = table2img_scatter(x, y, z, title, y_limit, aspect_ratio[ratio_id])
        mask_path_foreground, mask_path_background = img2mask_scatter(x, y, z, y_limit, aspect_ratio[ratio_id])
    d = extract_kw_similar(title)
    wordcloud_gen = WordCloudGenerator(font_path='C:/Users/user/A-project/speak/frontend/src/assets/fonts/TiltNeon-Regular.ttf',  
                                    background_color='#F5F5F5', colormap="binary",  
                                    prefer_horizontal=1, 
                                    max_font_size=45, min_font_size=12, 
                                    width=420, height=200, 
                                    margin=50, d=d)
    img_path2 = wordcloud_gen.generate_wordcloud()
    return [img_path1, img_path2, mask_path_foreground, mask_path_background]

@app.route('/generate_element',methods=['GET', 'POST'])
def generate_element():
    data = request.get_json()
    num_to_generate = data["num_to_generate"]
    method_to_generate = data["method_to_generate"]
    object_info = data["object"]
    description = data["description"]
    chart_bool_list = data["chart_type"]
    location = data["location"]
    print(data)

    prompt = object_info + ", " + description
    chart_type_list = ["bar", "line", "pie", "scatter"]
    if all(element is None for element in chart_bool_list):
        chart_type = "line"
    else:
        chart_type = chart_type_list[chart_bool_list.index(True)]

    global figure_size
    if figure_size and figure_size[0] < 10:
        figure_size = tuple([int(i * 96) for i in figure_size])
    else:
        figure_size = figure_size or (512, 512)
    print(figure_size)
    
    img_list = []
    
    if method_to_generate == "B" and location == "UNC":
        # print("B-UNC")
        img_list = text2img(pipe_text2img, prompt, figure_size, num_to_generate)
        print(type(img_list), len(img_list))
    
    if method_to_generate == "F" and location == "UNC":
        candidates_list = text2img(pipe_text2img, prompt, figure_size, num_to_generate)
        for i, image_pil in enumerate(candidates_list):
            img_list.append(extract_element(image_pil, object_info))

    if method_to_generate == "F" and location == "C":
        mask_path = data["mask"].replace("src/assets", "output")
        mask_pil = Image.open(mask_path).convert('RGB')
        if chart_type == "bar":
            match = re.search(r'_\d', mask_path)
            mask_single_FLAG = match is not None
            print("mask_single_FLAG: ", mask_single_FLAG)
            bar_ssistant = BarAssistant(strength=0.85)
            img_list = bar_ssistant(pipe_depth, pipe_paint, pipe_text2img, pipe_img2img, prompt, mask_pil, num_to_generate, mask_single_FLAG)
        if chart_type == "line":
            match = re.search(r'mask1.png', mask_path)
            mask_line_FLAG = match is not None
            print("mask_line_FLAG: ", mask_line_FLAG)
            line_ssistant = LineAssistant()
            img_list = line_ssistant(pipe_depth, pipe_paint, pipe_text2img, pipe_img2img, mask_pil, object_info, prompt, figure_size, mask_line_FLAG, num_to_generate)
        if chart_type == "scatter":
            match = re.search(r'_\d', mask_path)
            mask_single_FLAG = match is not None
            print("mask_single_FLAG: ", mask_single_FLAG)
            scatter_ssistant = ScatterAssistant()
            img_list = scatter_ssistant(pipe_depth, pipe_paint, pipe_text2img, pipe_img2img, mask_pil, object_info, prompt, figure_size, mask_single_FLAG, num_to_generate)
        if chart_type == "pie":
            pie_ssistant = PieAssistant()
            img_list = pie_ssistant(pipe_depth, pipe_paint, pipe_text2img, pipe_img2img, mask_pil, object_info, prompt, figure_size, num_to_generate)

    if method_to_generate == "B" and location == "C":
        print(data["mask"])
        mask_path = data["mask"].replace("src/assets", "output")
        mask_pil = Image.open(mask_path).convert('RGB')
        if chart_type == "bar":
            bar_ssistant = BarAssistant_B(strength=0.85)
            img_list = bar_ssistant(pipe_depth, pipe_paint, pipe_text2img, pipe_img2img, prompt, mask_pil, num_to_generate)
        if chart_type == "line":
            match = re.search(r'\b1\b', mask_path)
            mask_line_FLAG = match is not None
            print("mask_line_FLAG: ", mask_line_FLAG)
            line_ssistant = LineAssistant_B()
            img_list = line_ssistant(pipe_depth, pipe_paint, pipe_text2img, pipe_img2img, mask_pil, object_info, prompt, figure_size, mask_line_FLAG, num_to_generate)
        if chart_type == "scatter":
            scatter_ssistant = ScatterAssistant_B()
            img_list = scatter_ssistant(pipe_depth, pipe_paint, pipe_text2img, pipe_img2img, mask_pil, object_info, prompt, figure_size, num_to_generate)
        if chart_type == "pie":
            pie_ssistant = PieAssistant_B()
            img_list = pie_ssistant(pipe_depth, pipe_paint, pipe_text2img, pipe_img2img, mask_pil, object_info, prompt, figure_size, num_to_generate)
        

    if type(img_list[0])!=str:
        html_img_list = [pil_to_data_uri(img) for img in img_list]
        return html_img_list
    else:
        return random.shuffle(img_list)

    # img_list = []
    # img_dir = "/src/assets/generation/"
    # for i in range(10):
    #     img_path = img_dir + str(i) + ".png"
    #     img_list.append(img_path)
    # items = random.sample(img_list, num_to_generate)
    # return items

@app.route('/refine_element',methods=['GET', 'POST'])
def refine_element():
    # 其实有可能是透明，有可能是不透明的哦
    data = request.get_json()
    num_to_generate = data["num_to_generate"]
    object_info = data["object"]
    description = data["description"]
    try:
        dataurl = data["data"]["src"]
    except:
        dataurl = data["data"]
    image = dataurl_to_pil(dataurl, output_path=None).convert("RGB")
    image.save("output/refine.png")

    bg_image, _, _ = add_margin(image)
    bg_image.save("output/refine1.png")
    generator = torch.Generator(device="cuda").manual_seed(random.randint(0,99999999)) 
    output = pipe_img2img(prompt = object_info+description, image=bg_image, strength=0.45, guidance_scale=7.5, 
                        generator=generator, num_images_per_prompt=num_to_generate, return_dict=True)
    # images.insert(0, init_image)
    images = output.images
    images[0].save("output/refine2.png")
    nfsw_checker = output.nsfw_content_detected
    img_list = [images[i] for i in range(len(nfsw_checker)) if not nfsw_checker[i]]
    
    # print("=======================")
    if type(img_list[0])!=str:
        html_img_list = [pil_to_data_uri(img) for img in img_list]
        return html_img_list
    else:
        return random.shuffle(img_list)

@app.route('/evaluate_element',methods=['GET', 'POST'])
def evaluate_element():
    data = request.get_json()
    print("count:", data["count"])
    mask_path = data["mask_path"].replace("src/assets", "output")
    chart_type = data["type"]
    count = data["count"]
    dataurl = data["image_data"]["src"]
    image = dataurl_to_pil(dataurl, output_path=None).convert("RGBA")
    image.save("output/to_be_evaluate.png")

    if chart_type == "Bar":
        match = re.search(r'_\d', mask_path)
        mask_single_FLAG = match is not None
        bar_eval = BarEvaluation()
        result = bar_eval(mask_path, mask_single_FLAG, count)

    if chart_type == "Line":
        match = re.search(r'mask1.png', mask_path)
        mask_line_FLAG = match is not None
        line_eval = LineEvaluation()
        
        result = line_eval(mask_path, mask_line_FLAG, count)

    # if chart_type == "Pie":
    #     pie_eval = PieEvaluation()
    #     result = pie_eval(mask_path, count)

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=88, debug=True)

    # if method_to_generate == "FE" and location == "UNC":
    #     for i in range(num_to_generate):
    #         img_text2img = text2img_element(pipe_text2img, prompt)
    #         img_list.append(extract_element(img_text2img))

    # if method_to_generate == "FE" and location == "C":
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

    # if method_to_generate == "B" and location == "UNC":
    #     for i in range(num_to_generate):
    #         img_text2img = pipe_text2img(prompt=prompt, width=figure_size[0], height=figure_size[1], guidance_scale=7.5).images[0]
    #         img_list.append(extract_element(img_text2img))

    # if method_to_generate == "B" and location == "C":
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


