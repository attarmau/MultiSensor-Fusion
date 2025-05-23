Dataset (Open Source): UEC FOOD 256 - http://foodcam.mobi/dataset256.html 
<img width="386" alt="Screenshot 2025-05-23 at 10 14 59 AM" src="https://github.com/user-attachments/assets/0906ef8a-ed34-497d-a126-2d93770c944d" />
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
## Model Training 

```
yolo task=detect mode=train model=yolo11n.pt data=/Users/judyhuang/Downloads/yolo11-eating/datasets/custom.yaml epochs=100 imgsz=640
```
<img width="970" alt="Screenshot 2025-05-23 at 10 13 38 AM" src="https://github.com/user-attachments/assets/bf878920-0e5e-48e9-a9cf-6c9332d87fc7" />
