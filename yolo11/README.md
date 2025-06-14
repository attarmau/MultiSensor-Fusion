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
This setup simplifies the training task to binary food detection, suitable for scenarios like detecting whether someone is eating
```
yolo task=detect mode=train model=yolo11n.pt data=/Users/judyhuang/Downloads/yolo11-eating/datasets/custom.yaml epochs=1 imgsz=640
```
## Model Training - Eating Detection
<img width="1105" alt="Screenshot 2025-05-23 at 7 17 20 PM" src="https://github.com/user-attachments/assets/15d67a1c-8838-4455-b6f6-fdfca31b5e23" />
<img width="558" alt="Screenshot 2025-05-23 at 7 23 33 PM" src="https://github.com/user-attachments/assets/bcaea181-f407-4286-9042-b82c22e3b1b7" />
<img width="972" alt="Screenshot 2025-05-23 at 7 23 42 PM" src="https://github.com/user-attachments/assets/ebeaaa64-aed0-4c57-9014-bb03bbc7164d" />
<img width="966" alt="Screenshot 2025-05-23 at 7 23 52 PM" src="https://github.com/user-attachments/assets/e42670b7-7c24-4704-ae5c-b4dd023d01b4" />

## Roboflow 

1. **Searched for Open Datasets**

   * browsed and selected relevant datasets on Roboflow for the **"eating" action**, focusing on object detection (e.g., person, food, fork, spoon, etc.)

2. **Combined or Chose a Dataset**

   * picked a dataset (or created a project) that includes the labels needed for detecting eating-related actions

3. **Used Roboflow's UI to Manage Data**

   * leveraged Roboflow’s **web UI** to:

     * Visualise images and bounding boxes
     * Clean, review, or modify annotations
     * (Optionally) augment data using built-in tools

4. **Exported Dataset for YOLOv8/YOLO11 Training**

   * used **“Download Dataset”**
   * Selected export format: `YOLOv5 PyTorch` (✔️ compatible with YOLOv8/YOLO11)
   * Set image size (e.g., 640), and downloaded the `.zip` file

5. **Prepared Training Files**

   * Unzipped the dataset, which included:

     ```
     /train/images/
     /train/labels/
     /valid/images/
     /valid/labels/
     data.yaml
     ```

6. **Began Training with YOLOv11**

   * Attempted training with:

     ```bash
     yolo task=detect mode=train model=yolo11n.pt data=path/to/data.yaml epochs=100 imgsz=640
     ```
   * Test  live webcam detection:  
     ```
     yolo task=detect mode=predict model=/Users/judyhuang/Downloads/yolo11-video-eating/runs/detect/train/weights/best.pt source=0
     yolo task=detect mode=predict model=/Users/judyhuang/Downloads/yolo11-video-eating/runs/detect/train/weights/best.pt source=0 show=True

      ```

![image](https://github.com/user-attachments/assets/cc924203-d7b0-4689-ba8a-73d7a7703823)
