import matplotlib.pyplot as plt
import numpy as np
import torch
import requests
from PIL import Image
from diffusers import StableDiffusionDepth2ImgPipeline
import os
import sys
import PIL
import matplotlib.pyplot as plt
os.environ["cuda_visible_devices"] = '0'
current_path = os.getcwd()


def load_image(path):
    return PIL.Image.open(path).convert("1")

def image_grid(imgs, rows, cols):
    # imgs is a list containing several PIL objects
    assert len(imgs) == rows * cols

    w, h = imgs[0].size
    grid = PIL.Image.new('RGB', size=(cols * w, rows * h))
    grid_w, grid_h = grid.size

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid

def add_margin(img):
    background = Image.new("RGB", (512, 512), "black")

    x = (background.width - img.width) // 2
    y = (background.height - img.height) // 2

    background.paste(img, (x, y))
    return background, x, y


pipe = StableDiffusionDepth2ImgPipeline.from_pretrained(
   "stabilityai/stable-diffusion-2-depth",
   torch_dtype=torch.float16,
).to("cuda")

current_path = os.path.dirname(os.getcwd())
img_pth = 'data/carrot.png'

init_image = PIL.Image.open(img_pth).convert('RGB')
w, h = init_image.size
init_image, x, y = add_margin(init_image)

generator = torch.Generator(device="cuda").manual_seed(42)
theme = "carrot"
prompt = "icon style"
prompt = "a photograph of" + theme + "against a black background," + prompt + "30mm, 1080p full HD, 4k, sharp focus."
n_propmt = "blurry, watermark, text, signature, frame, cg render, lights"
images = pipe(prompt=prompt,
              image= init_image,
              negative_prompt=n_propmt,
              strength=0.375,
              num_images_per_prompt=3, generator=generator).images
images.insert(0, init_image)
images_r = image_grid(images, 1, len(images))
images_r.save('output/generation/gen.png')
