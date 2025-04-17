import cv2
import numpy as np
import glob
import argparse
import json
import os

def find_chessboard_corners(image_path, board_size):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, board_size, None)
    if ret:
        corners = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1),
            (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001))
    return ret, corners, gray.shape[::-1]

def calibrate_camera(image_folder, board_size, square_size):
    objp = np.zeros((board_size[0]*board_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2)
    objp *= square_size

    objpoints = []
    imgpoints = []
    image_size = None

    images = sorted(glob.glob(os.path.join(image_folder, '*.jpg')))

    for fname in images:
        ret, corners, img_size = find_chessboard_corners(fname, board_size)
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)
            image_size = img_size
        else:
            print(f"[WARN] Chessboard not found in {fname}")

    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, image_size, None, None)

    return camera_matrix, dist_coeffs

def save_intrinsics(filename, mtx, dist):
    data = {
        'camera_matrix': mtx.tolist(),
        'dist_coeffs': dist.tolist()
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--images', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--square', type=float, default=0.0244)
    parser.add_argument('--board', default='9x6')

    args = parser.parse_args()
    board_size = tuple(map(int, args.board.split('x')))

    mtx, dist = calibrate_camera(args.images, board_size, args.square)
    save_intrinsics(args.out, mtx, dist)

    print(f"[INFO] Calibration saved to {args.out}")
