import cv2
import numpy as np
import json
import os
import glob

def load_intrinsics(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    camera_matrix = np.array(data['camera_matrix'], dtype=np.float32)
    dist_coeffs = np.array(data['dist_coeffs'], dtype=np.float32)
    return camera_matrix, dist_coeffs

def find_chessboard_corners(image_path, board_size):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, board_size, None)
    if ret:
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                   (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001))
    return ret, corners, gray.shape[::-1]

def stereo_calibrate(cam1_images, cam2_images, board_size, square_size, cam1_intrinsics, cam2_intrinsics):
    objp = np.zeros((board_size[0] * board_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2)
    objp *= square_size

    objpoints = []
    imgpoints_cam1 = []
    imgpoints_cam2 = []
    image_size = None

    # 確保兩台相機的標定圖像數量相等
    if len(cam1_images) != len(cam2_images):
        print("[ERROR] The number of images from both cameras must be the same!")
        return None, None, None, None

    for cam1_img, cam2_img in zip(cam1_images, cam2_images):
        ret1, corners1, img_size = find_chessboard_corners(cam1_img, board_size)
        ret2, corners2, _ = find_chessboard_corners(cam2_img, board_size)

        if ret1 and ret2:
            objpoints.append(objp)
            imgpoints_cam1.append(corners1)
            imgpoints_cam2.append(corners2)
            image_size = img_size
        else:
            print(f"[WARN] Chessboard not found in {cam1_img} or {cam2_img}")

    if not objpoints:
        print("[ERROR] No valid chessboard corners detected. Ensure images are clear and chessboard is visible.")
        return None, None, None, None

    # 計算相機外參
    ret, camera_matrix1, dist_coeffs1, camera_matrix2, dist_coeffs2, R, T, E, F = cv2.stereoCalibrate(
        objpoints, imgpoints_cam1, imgpoints_cam2, cam1_intrinsics[0], cam1_intrinsics[1],
        cam2_intrinsics[0], cam2_intrinsics[1], image_size, flags=cv2.CALIB_FIX_INTRINSIC)

    if not ret:
        print("[ERROR] Stereo calibration failed. Check the images and try again.")
        return None, None, None, None

    return R, T, E, F

def save_extrinsics(filename, R, T):
    data = {
        'rotation': R.tolist(),
        'translation': T.tolist()
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    cam1_folder = '/path/to/cam1/images'
    cam2_folder = '/path/to/cam2/images'
    board_size = (9, 6)  # 9x6 inner corners
    square_size = 0.0244  # Square size in meters (adjust as needed)

    # 讀取內參
    cam1_intrinsics = load_intrinsics('intrinsics_cam1.json')
    cam2_intrinsics = load_intrinsics('intrinsics_cam2.json')

    # 讀取相機標定圖像
    cam1_images = sorted(glob.glob(os.path.join(cam1_folder, '*.jpg')))
    cam2_images = sorted(glob.glob(os.path.join(cam2_folder, '*.jpg')))

    # 執行雙目標定
    R, T, E, F = stereo_calibrate(cam1_images, cam2_images, board_size, square_size, cam1_intrinsics, cam2_intrinsics)

    if R is not None and T is not None:
        save_extrinsics('extrinsics_cam1_cam2.json', R, T)
        print("[INFO] Stereo calibration complete. Extrinsics saved to 'extrinsics_cam1_cam2.json'.")
    else:
        print("[ERROR] Calibration failed.")
