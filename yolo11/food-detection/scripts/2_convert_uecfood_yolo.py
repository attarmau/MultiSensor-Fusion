import os
import shutil
from PIL import Image

RAW_DATASET_DIR = "/Users/judyhuang/Downloads/yolo11-eating/datasets/raw_data"
OUTPUT_IMAGES_DIR = "/Users/judyhuang/Downloads/yolo11-eating/datasets/yolo_dataset/images"
OUTPUT_LABELS_DIR = "/Users/judyhuang/Downloads/yolo11-eating/datasets/yolo_dataset/labels"
CLASSES_TXT = "/Users/judyhuang/Downloads/yolo11-eating/datasets/classes.txt" 

with open(CLASSES_TXT, "r") as f:
    class_names = [line.strip() for line in f.readlines()]
category_name_to_id = {name: idx for idx, name in enumerate(class_names)}

for split in ['train', 'val']:
    os.makedirs(os.path.join(OUTPUT_IMAGES_DIR, split), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_LABELS_DIR, split), exist_ok=True)

def convert_to_yolo(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x_center = (box[0] + box[2]) / 2.0 * dw
    y_center = (box[1] + box[3]) / 2.0 * dh
    w = (box[2] - box[0]) * dw
    h = (box[3] - box[1]) * dh
    return x_center, y_center, w, h

all_images = []
for folder in os.listdir(RAW_DATASET_DIR):
    folder_path = os.path.join(RAW_DATASET_DIR, folder)
    if not os.path.isdir(folder_path):
        continue

    bb_info_path = os.path.join(folder_path, "bb_info.txt")
    if not os.path.exists(bb_info_path):
        continue

    label_id = int(folder) - 1  # YOLO classes are 0-indexed

    with open(bb_info_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            img_name = parts[0] + ".jpg"
            img_path = os.path.join(folder_path, img_name)
            if not os.path.exists(img_path):
                continue

            x1, y1, x2, y2 = map(int, parts[1:])
            try:
                img = Image.open(img_path)
                w, h = img.size
            except:
                continue

            yolo_box = convert_to_yolo((w, h), (x1, y1, x2, y2))

            all_images.append((img_path, label_id, yolo_box))

# Simple split: 90% train, 10% val
split_idx = int(0.9 * len(all_images))
train_data = all_images[:split_idx]
val_data = all_images[split_idx:]

def save_data(data, split):
    for i, (img_path, label_id, yolo_box) in enumerate(data):
        img_name = f"{split}_{i}.jpg"
        label_name = f"{split}_{i}.txt"

        # Copy image
        shutil.copy(img_path, os.path.join(OUTPUT_IMAGES_DIR, split, img_name))

        # Save label
        with open(os.path.join(OUTPUT_LABELS_DIR, split, label_name), "w") as f:
            f.write(f"{label_id} {' '.join(map(str, yolo_box))}\n")

save_data(train_data, "train")
save_data(val_data, "val")

print("!!! Conversion completed. Data saved to yolo_dataset/")
