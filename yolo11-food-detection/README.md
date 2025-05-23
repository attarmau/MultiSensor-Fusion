Dataset (Open Source): UEC FOOD 256 - http://foodcam.mobi/dataset256.html 
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
