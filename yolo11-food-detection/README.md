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
│   └── custom.yaml   ← your dataset config file
├── runs/              ← will be auto-created after training
│   └── detect/        ← results of training and validation
├── yolov11n.pt        ← your model file (pretrained, downloaded)
└── train.py (optional)  ← if you want to run training in script
```
