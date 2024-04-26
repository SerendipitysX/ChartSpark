import numpy as np
import torch
import PIL
import os


def clear_folder():
    main_folder = "C:/Users/user/A-project/speak/"
    folder_path = ["output/mask/bar/background", "output/mask/bar/foreground",
                  "output/mask/line/background", "output/mask/line/foreground",
                  "output/mask/pie/background", "output/mask/pie/foreground",
                  "frontend/src/assets/mask/bar/background", "frontend/src/assets/mask/bar/foreground",
                  "frontend/src/assets/mask/line/background", "frontend/src/assets/mask/line/foreground",
                  "frontend/src/assets/mask/pie/background", "frontend/src/assets/mask/pie/foreground",
                  "frontend/src/assets/evaluation"]  # 文件夹路径

    # 遍历文件夹中的所有文件并删除
    for i in range(len(folder_path)):
        for filename in os.listdir(main_folder+folder_path[i]):
            print(filename)
            file_path = os.path.join(main_folder, folder_path[i], filename)
            print(file_path)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")


def image_grid(imgs, rows, cols):
    # imgs is a list containing several PIL objects
    assert len(imgs) == rows * cols

    w, h = imgs[0].size
    grid = PIL.Image.new('RGB', size=(cols * w, rows * h))
    grid_w, grid_h = grid.size

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid


def load_image(path):
    return PIL.Image.open(path).convert("RGB")


