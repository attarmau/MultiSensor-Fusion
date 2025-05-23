This project uses YOLOv11 for "eating detection" based on labeled images in YOLO format.

Dataset (Open Source): UEC FOOD 256 - http://foodcam.mobi/dataset256.html 

<img width="386" alt="Screenshot 2025-05-23 at 10 14 59 AM" src="https://github.com/user-attachments/assets/0906ef8a-ed34-497d-a126-2d93770c944d" />

## Download Yolo (v8 -> v11)
When using YOLOv8, typically install the ultralytics package like this:
```
pip install ultralytics
```
Then you train your model using:
```
yolo task=detect mode=train model=yolov8n.pt data=path/to/custom.yaml epochs=100 imgsz=640
```
Note: You could use yolov8n.pt, yolov8s.pt, etc.

Starting in 2024, Ultralytics released YOLOv11 — the next generation of YOLO. To get YOLOv11, you need the latest version of the ultralytics package. So you upgrade:
```
pip install -U ultralytics
```
Once upgraded, YOLOv11 models are available and you use them like this:
```
yolo task=detect mode=train model=yolov11n.pt data=path/to/custom.yaml epochs=100 imgsz=640
```

## Model Training - Food Detection 

<img width="976" alt="Screenshot 2025-05-23 at 10 16 53 AM" src="https://github.com/user-attachments/assets/9580fa2f-6e0c-4616-a8f3-bcc194c3fb74" />


```
yolo task=detect mode=train model=yolo11n.pt data=/Users/judyhuang/Downloads/yolo11-eating/datasets/custom.yaml epochs=100 imgsz=640
```
<img width="970" alt="Screenshot 2025-05-23 at 10 13 38 AM" src="https://github.com/user-attachments/assets/bf878920-0e5e-48e9-a9cf-6c9332d87fc7" />

## Folder Structure

```
yolo11-food-detection/
├── datasets/
│   ├── yolo_dataset
│   │   ├── images/
│   │   │   ├── train/
│   │   │   │   ├── img1.jpg
│   │   │   │   └── ...
│   │   │   ├── val/
│   │   │   │   ├── img2.jpg
│   │   │   │   └── ...
│   │   ├── labels/
│   │   │   ├── train/
│   │   │   │   ├── img1.txt
│   │   │   │   └── ...
│   │   │   ├── val/
│   │   │   │   ├── img2.txt
│   │   └── ──  └── ...
│   ├── classes.txt
│   └── custom.yaml    ← dataset config file
├── runs/              ← will be auto-created after training
│   └── detect/        ← results of training and validation
└── yolov11n.pt        ← model file (pretrained, downloaded)
```
## However, the projet is to 'detect whether food is present in the scene' — not classify the specific food
To achieve this

1. relabel all annotations to a single class (food):
```
python 5_convert_all_class_to_0.py
```
<img width="383" alt="Screenshot 2025-05-23 at 3 19 31 PM" src="https://github.com/user-attachments/assets/1fe73c51-7ff9-4ebf-8237-6e9730b4b482" />

2. Updated the YOLO dataset YAML:
```
path: /Your/Dataset/Path
train: images/train
val: images/val

names:
  0: food
```
This setup simplifies the training task to binary food detection — perfect for scenarios like detecting whether someone is eating
