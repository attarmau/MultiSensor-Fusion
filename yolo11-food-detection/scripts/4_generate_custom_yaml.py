import yaml

def generate_custom_yaml(classes_path, yaml_output_path, train_path='datasets/images/train', val_path='datasets/images/val'):
    with open(classes_path, 'r', encoding='utf-8') as f:
        class_names = [line.strip() for line in f.readlines() if line.strip()]

    yaml_dict = {
        'path': 'datasets',
        'train': train_path,
        'val': val_path,
        'names': class_names
    }

    with open(yaml_output_path, 'w', encoding='utf-8') as outfile:
        yaml.dump(yaml_dict, outfile, allow_unicode=True)

    print(f"✅ Created {yaml_output_path} with {len(class_names)} classes.")

generate_custom_yaml('../datasets/classes.txt', '../datasets/custom.yaml')
