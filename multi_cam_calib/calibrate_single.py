import os
import glob
import json
import numpy as np
import cv2

with open('/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/intrinsics_cam1.json', 'r') as f:
    data1 = json.load(f)
camera_matrix1 = np.array(data1['camera_matrix'])
dist_coeffs1 = np.array(data1['dist_coeffs'])

with open('/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/intrinsics_cam2.json', 'r') as f:
    data2 = json.load(f)
camera_matrix2 = np.array(data2['camera_matrix'])
dist_coeffs2 = np.array(data2['dist_coeffs'])

input_dir_cam1 = '/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/intrinsic/cam1'
output_dir_cam1 = '/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/intrinsic/undistorted_cam1'
input_dir_cam2 = '/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/intrinsic/cam2'
output_dir_cam2 = '/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/intrinsic/undistorted_cam2'

os.makedirs(output_dir_cam1, exist_ok=True)
os.makedirs(output_dir_cam2, exist_ok=True)

for img_path in glob.glob(os.path.join(input_dir_cam1, '*.jpg')):
    img = cv2.imread(img_path)
    if img is not None:
        undistorted = cv2.undistort(img, camera_matrix1, dist_coeffs1)
        filename = os.path.basename(img_path)
        save_path = os.path.join(output_dir_cam1, f'undistorted_{filename}')
        cv2.imwrite(save_path, undistorted)
        print(f"[INFO] Saved undistorted image: {save_path}")
    else:
        print(f"[ERROR] Could not load image: {img_path}")

for img_path in glob.glob(os.path.join(input_dir_cam2, '*.jpg')):
    img = cv2.imread(img_path)
    if img is not None:
        undistorted = cv2.undistort(img, camera_matrix2, dist_coeffs2)
        filename = os.path.basename(img_path)
        save_path = os.path.join(output_dir_cam2, f'undistorted_{filename}')
        cv2.imwrite(save_path, undistorted)
        print(f"[INFO] Saved undistorted image: {save_path}")
    else:
        print(f"[ERROR] Could not load image: {img_path}")
