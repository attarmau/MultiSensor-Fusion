# Multi-Sensor-Fusion
## non-rigid multi-camera pose estimation

This repo performs stereo calibration for a two-camera setup using OpenCV. It computes intrinsic and extrinsic parameters to align both cameras into a shared coordinate frame.

![2025-04-20 10 42 48](https://github.com/user-attachments/assets/c46f2234-b7b9-40a4-916c-1feef68c3a92)



## Setup

```bash
pip install -r requirements.txt
```
## Folder Structure
```
Multi-Sensor-Fusion/
├── multi_cam_calib/
│   ├── calibrate_single.py        # Calibrate each camera separately
│   ├── intrinsics_cam0.json
│   ├── intrinsics_cam1.json
│   ├── calibrate_stereo.py        # Compute extrinsics between two cameras
│   ├── extrinsics_cam1_cam2.json  # Stores stereo calibration results
│   └── utils.py                   # Helper functions
│
├── data/
│   ├── cam0/                      # Calibration images from camera 0
│   │   ├── img_001.jpg
│   │   └── ...
│   └── cam1/                      # Calibration images from camera 1
│       ├── img_001.jpg
│       └── ...
│
├── README.md                      # Setup + usage instructions
├── requirements.txt               # Dependencies
└── .gitignore
```

Camera calibration finds the intrinsic parameters of your camera, like:
- fx, fy: focal length (in pixels)
- cx, cy: principal point (optical center)
- k1, k2, ...: lens distortion coefficients

These parameters describe how your camera "sees" the world and are essential for:
- 3D reconstruction
- Multi-camera fusion
- Removing lens distortion
- Projecting 3D points onto 2D images accurately

# Run 
## Step 1: Get the intrinsic parameters
```
  --images /Your-file-path/MultiSensor-Fusion-main/data/cam1 \
  --out intrinsics_cam1.json \
  --board 9x6
```
If it shows the message below then means the intrinsic parameters were saved successfully
```
[INFO] Calibration saved to intrinsics_cam1.json
```
## Step 2: Get the extrinsic parameters
```
python calibrate_stereo.py
```
If it shows the message below then means the extrinsic parameters were saved successfully
```
[INFO] Stereo calibration complete. Extrinsics saved to 'extrinsics_cam1_cam2.json'.
```
