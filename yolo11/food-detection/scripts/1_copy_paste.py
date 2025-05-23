import os
import shutil
from pathlib import Path

def flatten_uecfood_structure(root_dir):
    image_out = os.path.join(root_dir, "images")
    label_out = os.path.join(root_dir, "labels")
    os.makedirs(image_out, exist_ok=True)
    os.makedirs(label_out, exist_ok=True)

    skip_folders = {'images', 'labels'}

    for category_id in os.listdir(root_dir):
        if category_id in skip_folders:
            continue  

        category_path = os.path.join(root_dir, category_id)
        if not os.path.isdir(category_path):
            continue

        for file in os.listdir(category_path):
            src_path = os.path.join(category_path, file)
            if not os.path.isfile(src_path):
                continue

            ext = Path(file).suffix.lower()
            if ext in ['.jpg', '.jpeg', '.png']:
                dst_path = os.path.join(image_out, file)
            elif ext == '.txt':
                dst_path = os.path.join(label_out, file)
            else:
                continue  

            if os.path.abspath(src_path) != os.path.abspath(dst_path):
                shutil.copy(src_path, dst_path)

    print(" Flattened folder structure into 'images/' and 'labels/'")

flatten_uecfood_structure('/Users/judyhuang/Downloads/yolo11-eating/datasets/uecfood')
