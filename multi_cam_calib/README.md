## Setup

```bash
pip install -r requirements.txt
```
## Folder Structure
```
Multi-Sensor-Fusion/
├── multi_cam_calib/
│   ├── calibrate_single.py          # Calibrate each camera separately
│   ├── calibrate_extrinsics_pnp.py  # Extrinsic estimation using PnP
│   ├── utils.py
│
├── data/
│   ├── intrinsics/                  # Intrinsic parameters for each camera in JSON format
│   │   ├── cam1/
│   │   │   ├── img_001.jpg
│   │   │   ├── img_002.jpg
│   │   │   └── ...
│   │   ├── cam2/
│   │   │   ├── img_001.jpg
│   │   │   ├── img_002.jpg
│   │   │   └── ...
│   │   ├── intrinsics_cam0.json
│   │   ├── intrinsics_cam1.json
│   │   └── ...
│   ├── extrinsic/                   # Image sets for extrinsic calibration
│   │   ├── set01/
│   │   │   ├── cam1.jpg
│   │   │   ├── cam2.jpg
│   │   │   └── ...
│   │   ├── set02/
│   │   │   ├── cam1.jpg
│   │   │   ├── cam2.jpg
│   │   │   └── ...
│   └── output/
│       └── extrinsics_multi_cam.json
│
├── README.md
└── requirements.txt
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
python /Users/judyhuang/Downloads/MultiSensor-Fusion-main/multi_cam_calib/calibrate_single.py \
  --images //Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/intrinsic/cam1 \
  --out /Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/intrinsics_cam1.json \
  --board 6x9
```
If it shows the message below then means the intrinsic parameters were saved successfully
```
[INFO] Calibration saved to intrinsics_cam1.json
```
More theory based intro of intrinsic matrix can refer to: https://ksimek.github.io/2013/08/13/intrinsic/

## Step 2: Get the extrinsic parameters
```
python calibrate_stereo.py
```
If it shows the message below then means the extrinsic parameters were saved successfully
```
[INFO] Stereo calibration complete. Extrinsics saved to 'extrinsics_cam1_cam2.json'.
```
Note: My scenario is 'Extrinsic Calibration for Fixed Multi-Camera Setup with Non-Movable Lenses'

In this setup, multiple cameras are fixed in different corners, and their lenses do not move. The goal is to estimate the relative positions and orientations (extrinsics) between cameras using images of a shared 3D calibration object (e.g., a chessboard). The script uses the Perspective-n-Point (PnP) method, based on known intrinsic parameters and the object’s geometry.

⚠️ If your cameras can move or are repositioned together (e.g., in a stereo rig), you will need to modify the Step 2 script to fit your setup accordingly.

Reference: https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
