import cv2
import numpy as np
import os
import json
from glob import glob

def load_intrinsics(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    camera_matrix = np.array(data['camera_matrix'], dtype=np.float32)
    dist_coeffs = np.array(data['dist_coeffs'], dtype=np.float32)
    return camera_matrix, dist_coeffs

def find_corners(image_path, board_size):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, board_size, None)
    if ret:
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
            (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001))
    return ret, corners

def generate_objpoints(board_size, square_size):
    objp = np.zeros((board_size[0]*board_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2)
    objp *= square_size
    return objp

def estimate_extrinsics(set_folder, cam_names, board_size, square_size, intrinsics_dir):
    objp = generate_objpoints(board_size, square_size)
    cam_results = {}

    for cam in cam_names:
        objpoints = []
        imgpoints = []

        image_paths = sorted(glob(os.path.join(set_folder, f"set*/{cam}.jpg")))
        camera_matrix, dist_coeffs = load_intrinsics(os.path.join(intrinsics_dir, f"intrinsics_{cam}.json"))

        for img_path in image_paths:
            ret, corners = find_corners(img_path, board_size)
            if ret:
                objpoints.append(objp)
                imgpoints.append(corners)
            else:
                print(f"[WARN] Chessboard not found in {img_path}")

        rvecs, tvecs = [], []
        for objp_i, imgp_i in zip(objpoints, imgpoints):
            ret, rvec, tvec = cv2.solvePnP(objp_i, imgp_i, camera_matrix, dist_coeffs)
            if ret:
                rvecs.append(rvec)
                tvecs.append(tvec)

        rvec_mean = np.mean(rvecs, axis=0)
        tvec_mean = np.mean(tvecs, axis=0)
        R, _ = cv2.Rodrigues(rvec_mean)

        cam_results[cam] = {
            "rotation": R.tolist(),
            "translation": tvec_mean.tolist(),
        }

    return cam_results

def save_results(output_path, results):
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    board_size = (9, 6)  # inner corners
    square_size = 0.0244  # meter
    set_folder = "shared_chessboard_sets"
    intrinsics_dir = "multi_cam_calib"
    cam_names = ["cam0", "cam1"]  # update if you have more cameras

    results = estimate_extrinsics(set_folder, cam_names, board_size, square_size, intrinsics_dir)
    save_results("extrinsics_multi_cam.json", results)
    print("[INFO] Extrinsic calibration complete. Saved to extrinsics_multi_cam.json")
