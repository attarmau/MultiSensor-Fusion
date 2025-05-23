import os
import shutil
import random

# === Config ===
base_dir = "/Users/judyhuang/Downloads/yolo11-eating/datasets/uecfood"
source_images = "dataset/images"     # original image path
source_labels = "dataset/labels"     # YOLO formatted label path
split_ratio = 0.8                    # 80% train, 20% val

# === Target folders ===
train_img_dir = os.path.join(base_dir, "images/train")
val_img_dir   = os.path.join(base_dir, "images/val")
train_lbl_dir = os.path.join(base_dir, "labels/train")
val_lbl_dir   = os.path.join(base_dir, "labels/val")

for d in [train_img_dir, val_img_dir, train_lbl_dir, val_lbl_dir]:
    os.makedirs(d, exist_ok=True)

# === Match image-label pairs ===
image_files = [f for f in os.listdir(source_images) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
image_files = sorted(image_files)  # for consistency

random.seed(42)
random.shuffle(image_files)

split_index = int(len(image_files) * split_ratio)
train_files = image_files[:split_index]
val_files   = image_files[split_index:]

def copy_pair(image_list, target_img_dir, target_lbl_dir):
    for img_file in image_list:
        name, _ = os.path.splitext(img_file)
        label_file = f"{name}.txt"

        img_src = os.path.join(source_images, img_file)
        lbl_src = os.path.join(source_labels, label_file)

        img_dst = os.path.join(target_img_dir, img_file)
        lbl_dst = os.path.join(target_lbl_dir, label_file)

        shutil.copy(img_src, img_dst)
        if os.path.exists(lbl_src):
            shutil.copy(lbl_src, lbl_dst)

copy_pair(train_files, train_img_dir, train_lbl_dir)
copy_pair(val_files, val_img_dir, val_lbl_dir)

print(f" !!!!Split complete: {len(train_files)} train / {len(val_files)} val")
