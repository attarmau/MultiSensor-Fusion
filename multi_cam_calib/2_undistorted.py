import os
import glob
import cv2
import numpy as np

camera_matrix1 = np.array([
    [1081.351931279377, 0.0, 503.24308280888977],
    [0.0, 1087.2102580661729, 389.88880849450794],
    [0.0, 0.0, 1.0]
])
dist_coeffs1 = np.array([
    -0.38495725519585405,
    0.29131295558148523,
    -0.0009713217982991812,
    -0.0006500813492399818,
    -0.1137841215152717
])

camera_matrix2 = np.array([
    [1084.5581207020903, 0.0, 396.9566288777321],
    [0.0, 1096.4221539054233, 394.12188684102887],
    [0.0, 0.0, 1.0]
])
dist_coeffs2 = np.array([
    -0.4342501698447082,
    0.4374503110656183,
    -0.0015619894083689551,
    0.0036684626844795767,
    -0.24472922059690175
])

input_dir_cam1 = '/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/intrinsic/cam1'
input_dir_cam2 = '/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/intrinsic/cam2'
output_dir_cam1 = '/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/intrinsic/undistorted_cam1'
output_dir_cam2 = '/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/intrinsic/undistorted_cam2'

os.makedirs(output_dir_cam1, exist_ok=True)
os.makedirs(output_dir_cam2, exist_ok=True)

image_paths_cam1 = sorted(glob.glob(os.path.join(input_dir_cam1, '*.jpg')))

for i in range(len(image_paths_cam1)):
    image_path_cam1 = image_paths_cam1[i]
    filename_cam1 = os.path.basename(image_path_cam1)

    image_path_cam2 = os.path.join(input_dir_cam2, filename_cam1)
    if not os.path.exists(image_path_cam2):
        print(f"[WARNING] No matching cam2 image for: {filename_cam1}")
        continue

    img1 = cv2.imread(image_path_cam1)
    img2 = cv2.imread(image_path_cam2)

    if img1 is None or img2 is None:
        print(f"[ERROR] Could not load image pair: {filename_cam1}")
        continue
      
    h1, w1 = img1.shape[:2]
    new_camera_matrix1, _ = cv2.getOptimalNewCameraMatrix(
        camera_matrix1, dist_coeffs1, (w1, h1), 1, (w1, h1)
    )
    undistorted1 = cv2.undistort(img1, camera_matrix1, dist_coeffs1, None, new_camera_matrix1)

    h2, w2 = img2.shape[:2]
    new_camera_matrix2, _ = cv2.getOptimalNewCameraMatrix(
        camera_matrix2, dist_coeffs2, (w2, h2), 1, (w2, h2)
    )
    undistorted2 = cv2.undistort(img2, camera_matrix2, dist_coeffs2, None, new_camera_matrix2)

    save_path_cam1 = os.path.join(output_dir_cam1, filename_cam1)
    save_path_cam2 = os.path.join(output_dir_cam2, filename_cam1)
    cv2.imwrite(save_path_cam1, undistorted1)
    cv2.imwrite(save_path_cam2, undistorted2)

    print(f"[INFO] Saved undistorted cam1 image: {save_path_cam1}")
    print(f"[INFO] Saved undistorted cam2 image: {save_path_cam2}")
