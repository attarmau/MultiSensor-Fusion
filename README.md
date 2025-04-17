# Multi-Sensor-Fusion

This repo performs stereo calibration for a two-camera setup using OpenCV. It computes intrinsic and extrinsic parameters to align both cameras into a shared coordinate frame.

## Setup

```bash
pip install -r requirements.txt
```
```
Multi-Sensor-Fusion/
├── camera_calibration/
│   ├── calibrate_single.py        # Calibrate each camera separately
│   ├── calibrate_stereo.py        # Compute extrinsics between two cameras
│   ├── stereo_config.json         # Stores stereo calibration results
│   ├── intrinsics_cam0.json
│   ├── intrinsics_cam1.json
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
