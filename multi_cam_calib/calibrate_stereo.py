import cv2
import numpy as np
import json
import glob
import os

def load_intrinsics(filename):
    """
    Load camera intrinsics from a JSON file.
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    camera_matrix = np.array(data['camera_matrix'], dtype=np.float32)
    dist_coeffs = np.array(data['dist_coeffs'], dtype=np.float32)
    return camera_matrix, dist_coeffs

def find_chessboard_corners(image_path, board_size):
    """
    Find the chessboard corners in an image.
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, board_size, None)
    if ret:
        corners = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1),
            (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001))
    return ret, corners, gray.shape[::-1]

def calibrate_extrinsics_pnp(cam1_images, cam2_images, board_size, square_size, cam1_intrinsics, cam2_intrinsics):
    """
    Perform extrinsics calibration using PnP (Perspective-n-Point) method.
    """
    objp = np.zeros((board_size[0]*board_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2)
    objp *= square_size

    objpoints = []
    imgpoints_cam1 = []
    imgpoints_cam2 = []
    image_size = None

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

    # Estimate extrinsics using PnP
    R_list = []
    T_list = []

    for objp_single, imgpoints_single_cam1, imgpoints_single_cam2 in zip(objpoints, imgpoints_cam1, imgpoints_cam2):
        # Estimate pose for cam1
        ret1, rvec1, tvec1 = cv2.solvePnP(objp_single, imgpoints_single_cam1, cam1_intrinsics[0], cam1_intrinsics[1])
        # Estimate pose for cam2
        ret2, rvec2, tvec2 = cv2.solvePnP(objp_single, imgpoints_single_cam2, cam2_intrinsics[0], cam2_intrinsics[1])

        if ret1 and ret2:
            R_list.append(rvec1)
            T_list.append(tvec1)
            R_list.append(rvec2)
            T_list.append(tvec2)

    return R_list, T_list

def save_extrinsics(filename, R_list, T_list):
    """
    Save the extrinsic parameters (rotation and translation) to a JSON file.
    """
    data = {
        'rotation': [rvec.tolist() for rvec in R_list],
        'translation': [tvec.tolist() for tvec in T_list]
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    # Set paths to the folders containing images from both cameras
    cam1_folder = '/path/to/cam1/images'
    cam2_folder = '/path/to/cam2/images'
    board_size = (9, 6)  # 9x6 inner corners
    square_size = 0.0244  # Square size in meters (adjust as needed)

    # Load the intrinsic parameters for both cameras
    cam1_intrinsics = load_intrinsics('intrinsics_cam1.json')
    cam2_intrinsics = load_intrinsics('intrinsics_cam2.json')

    # Get the list of calibration images for both cameras
    cam1_images = sorted(glob.glob(os.path.join(cam1_folder, '*.jpg')))
    cam2_images = sorted(glob.glob(os.path.join(cam2_folder, '*.jpg')))

    # Perform extrinsics calibration using PnP
    R_list, T_list = calibrate_extrinsics_pnp(cam1_images, cam2_images, board_size, square_size, cam1_intrinsics, cam2_intrinsics)

    # Save the extrinsic parameters (rotation and translation)
    save_extrinsics('extrinsics_pnp.json', R_list, T_list)
    print("[INFO] Extrinsics calibration complete. Parameters saved to 'extrinsics_pnp.json'.")
