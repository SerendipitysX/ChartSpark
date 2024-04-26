from omegaconf import OmegaConf
import torch
from PIL import Image
from torchvision import transforms
import os
import math
from tqdm import tqdm
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import importlib
import os
from PIL import Image
import PIL
import numpy as np
import torch
from torch import nn, einsum
from einops import rearrange
import math
from generation.ldm.modules.attention import CrossAttention
import sys
current_path = os.getcwd()
sys.path.append(os.path.join(current_path, 'generation\ldm'))


def get_obj_from_str(string, reload=False):    
    module, cls = string.rsplit(".", 1)
    if reload:        
        module_imp = importlib.import_module(module)
        importlib.reload(module_imp)    
    return getattr(importlib.import_module(module, package=None), cls)

def instantiate_from_config(config):    
    if not "target" in config:
        if config == '__is_first_stage__':            
            return None
        elif config == "__is_unconditional__":            
            return None
        raise KeyError("Expected key `target` to instantiate.")    
    return get_obj_from_str(config["target"])(**config.get("params", dict()))

def load_model_from_config(config, ckpt, device="cpu", verbose=False):
    """Loads a model from config and a ckpt
    if config is a path will use omegaconf to load
    """
    if isinstance(config, (str, Path)):
        config = OmegaConf.load(config)

    pl_sd = torch.load(ckpt, map_location="cpu")
    global_step = pl_sd["global_step"]
    sd = pl_sd["state_dict"]
    model = instantiate_from_config(config.model)
    m, u = model.load_state_dict(sd, strict=False)
    model.to(device)
    model.eval()
    model.cond_stage_model.device = device
    return model

@torch.no_grad()
def sample_model(model, sampler, c, h, w, ddim_steps, scale, ddim_eta, start_code=None, n_samples=1):
    """Sample the model"""
    uc = None
    if scale != 1.0:
        uc = model.get_learned_conditioning(n_samples * [""])

    shape = [4, h // 8, w // 8]
    samples_ddim, _ = sampler.sample(S=ddim_steps,
                                     conditioning=c,
                                     batch_size=n_samples,
                                     shape=shape,
                                     verbose=False,
                                     start_code=start_code,
                                     unconditional_guidance_scale=scale,
                                     unconditional_conditioning=uc,
                                     eta=ddim_eta,
                                    )
    return samples_ddim

def load_img(path, target_size=512):
    """Load an image, resize and output -1..1"""
    image = Image.open(path).convert("RGB")
    
    
    tform = transforms.Compose([
            transforms.Resize(target_size),
            transforms.CenterCrop(target_size),
            transforms.ToTensor(),
        ])
    image = tform(image)
    return 2.*image - 1.

# def decode_to_im(samples, n_samples=1, nrow=1):
    """Decode a latent and return PIL image"""
    samples = model.decode_first_stage(samples)
    ims = torch.clamp((samples + 1.0) / 2.0, min=0.0, max=1.0)
    x_sample = 255. * rearrange(ims.cpu().numpy(), '(n1 n2) c h w -> (n1 h) (n2 w) c', n1=n_samples//nrow, n2=nrow)
    return Image.fromarray(x_sample.astype(np.uint8))
    
# def update_layer_names(model):
#     hidden_layers = {}
#     for n, m in model.named_modules():
#         if(isinstance(m, CrossAttention)):
#             hidden_layers[n] = m
#     hidden_layer_names = list(filter(lambda s : "attn2" in s, hidden_layers.keys())) 
#     if hidden_layer_select != None:
#         hidden_layer_select.update(value=default_hidden_layer_name, choice=hidden_layer_names)

def get_attn(emb, ret):
    def hook(self, sin, sout):
        h = self.heads
        q = self.to_q(sin[0])
        context = emb
        k = self.to_k(context)
        q, k = map(lambda t: rearrange(t, 'b n (h d) -> (b h) n d', h=h), (q, k))
        sim = einsum('b i d, b j d -> b i j', q, k) * self.scale
        attn = sim.softmax(dim=-1)
        ret["out"] = attn
    return hook

def generate_vxa(image, prompt, idx, time, layer_name, output_mode, model, hidden_layers):
    if(not isinstance(image, np.ndarray)):
        print("if(not isinstance(image, np.ndarray))")
        return image
    output = image.copy()
    image = image.astype(np.float32) / 255.0
    image = np.moveaxis(image, 2, 0)
    image = torch.from_numpy(image).unsqueeze(0)

    layer = hidden_layers[layer_name]
    cond_model = model.cond_stage_model
    with torch.no_grad():
        image = image.to("cuda")
        latent = model.get_first_stage_encoding(model.encode_first_stage(image))
        try:
            t = torch.tensor([float(time)]).to("cuda")
        except:
            print("t有问题")
            return output
        emb = cond_model([prompt])

        attn_out = {}
        handle = layer.register_forward_hook(get_attn(emb, attn_out))
        try:
            model.apply_model(latent, t, emb)
        finally:
            handle.remove()
            
    if (idx == ""):
        img = attn_out["out"][:,:,1:].sum(-1).sum(0)
    else:
        try:
            idxs = list(map(int, filter(lambda x : x != '', idx.strip().split(','))))
            img = attn_out["out"][:,:,idxs].sum(-1).sum(0)
        except:
            print("idx有问题")
            return output
    # print(img.shape)
    scale = round(math.sqrt((image.shape[2] * image.shape[3]) / img.shape[0]))
    h = image.shape[2] // scale
    w = image.shape[3] // scale
    img = img.reshape(h, w) / img.max()
    img = img.to("cpu").numpy()
    # print(img.shape)
    output = output.astype(np.float64)
    if output_mode == "masked":
        for i in range(output.shape[0]):
            for j in range(output.shape[1]):
                output[i][j] *= img[i // scale][j // scale]
    elif output_mode == "grey":
        for i in range(output.shape[0]):
            for j in range(output.shape[1]):
                output[i][j] = [img[i // scale][j // scale] * 255.0] * 3
    output = output.astype(np.uint8)
    # print("end")
    return output, img

def get_attn_mask(input_image, vxa_prompt, model, hidden_layers):
    input_image = np.array(input_image)
    vxa_token_indices = ""
    vxa_time_embedding = 1.0
    for n, m in model.named_modules():
        if(isinstance(m, CrossAttention)):
            hidden_layers[n] = m
    hidden_layer_names = list(filter(lambda s : "attn2" in s, hidden_layers.keys()))
    hidden_layer_select = hidden_layer_names[6]
    vxa_output_mode = "-" # choices=["masked", "grey"]
    output = generate_vxa(input_image, vxa_prompt, vxa_token_indices, vxa_time_embedding, hidden_layer_select, vxa_output_mode, model, hidden_layers)
    return output