import cv2
import numpy as np
import glob
import argparse
import json
import os

def calibrate_camera(image_folder, board_size, square_size):
    objp = np.zeros((board_size[0]*board_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2)
    objp *= square_size

    objpoints = []
    imgpoints = []

    images = sorted(glob.glob(os.path.join(image_folder, '*.jpg')))

    for fname in images:
        img = cv2.imread(fname)
        if img is None:
            print(f'[WARN] Could not read {fname}')
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(
            gray, board_size,
            cv2.CALIB_CB_ADAPTIVE_THRESH + 
            cv2.CALIB_CB_FAST_CHECK + 
            cv2.CALIB_CB_NORMALIZE_IMAGE)
            
        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(
                gray, corner, (11, 11), (-1, -1),
                (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
            imgpoints.append(corners)

            vis_img = cv2.drawChessboardCorners(img, board_size, corners2, ret)
            cv2.imshow('Corners', vis_img)
            cv2.waitKey(500)
        else:
            print(f"[WARN] Chessboard not found in {fname}")

    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None)

    return camera_matrix, dist_coeffs

def save_intrinsics(filename, camera_matrix, dist_coeffs, rvecs, tvecs):
    data = {
        'camera_matrix': camera_matrix.tolist(),
        'dist_coeffs': dist_coeffs.tolist(),
        'rotation_vectors': [rvec.tolist() for rvec in rvecs],
        'translation_vectors': [tvec.tolist() for tvec in tvecs]
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--images', required=True, help='Path to folder containing chessboard images')
    parser.add_argument('--out', required=True, help='Output JSON file for intrinsics')
    parser.add_argument('--square', type=float, default=0.0244, help='Chessboard square size in meters')
    parser.add_argument('--board', default='6x9', help='Chessboard size as colsxrows (e.g. 6x9)')

    args = parser.parse_args()
    board_size = tuple(map(int, args.board.split('x')))

    print(f"[INFO] Using board size: {board_size}")
    print(f"[INFO] Using square size: {args.square} meters")

    camera_matrix, dist_coeffs, rvecs, tvecs = calibrate_camera(args.images, board_size, args.square)
    save_intrinsics(args.out, camera_matrix, dist_coeffs, rvecs, tvecs)

    print(f"[INFO] Calibration complete. Results saved to {args.out}")
    print(f"[INFO] Camera matrix:\n{camera_matrix}")
    print(f"[INFO] Distortion coefficients:\n{dist_coeffs}")
