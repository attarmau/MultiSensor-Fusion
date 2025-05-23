import os

# Set to your labels base directory
label_base_dir = "/Users/judyhuang/Downloads/yolo11-eating/datasets/uecfood/labels"

for split in ['train', 'val']:
    split_dir = os.path.join(label_base_dir, split)
    for file_name in os.listdir(split_dir):
        if not file_name.endswith(".txt"):
            continue
        path = os.path.join(split_dir, file_name)
        with open(path, 'r') as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 5:
                parts[0] = '0'  # Overwrite class ID with 0
                new_lines.append(' '.join(parts))
        with open(path, 'w') as f:
            f.write('\n'.join(new_lines))
print("✅ All label files converted to single class: 'food'")