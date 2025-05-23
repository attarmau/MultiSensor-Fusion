```
yolo11-eating/
├── datasets/
│   ├── images/
│   │   ├── train/
│   │   │   ├── img1.jpg
│   │   │   └── ...
│   │   ├── val/
│   │   │   ├── img2.jpg
│   │   │   └── ...
│   ├── labels/
│   │   ├── train/
│   │   │   ├── img1.txt
│   │   │   └── ...
│   │   ├── val/
│   │   │   ├── img2.txt
│   │   │   └── ...
│   └── custom.yaml    ← dataset config file
├── runs/              ← will be auto-created after training
│   └── detect/        ← results of training and validation
└── yolov11n.pt        ← model file (pretrained, downloaded)
```
