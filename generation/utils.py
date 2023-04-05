from omegaconf import OmegaConf
import torch
from PIL import Image
from torchvision import transforms
import os
from tqdm import tqdm
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import importlib


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

def decode_to_im(samples, n_samples=1, nrow=1):
    """Decode a latent and return PIL image"""
    samples = model.decode_first_stage(samples)
    ims = torch.clamp((samples + 1.0) / 2.0, min=0.0, max=1.0)
    x_sample = 255. * rearrange(ims.cpu().numpy(), '(n1 n2) c h w -> (n1 h) (n2 w) c', n1=n_samples//nrow, n2=nrow)
    return Image.fromarray(x_sample.astype(np.uint8))
    
    