import cv2, glob, numpy as np
from utils import find_chessboard_corners

# Loop through image set per camera
def calibrate_camera(image_dir, board_size=(9,6), square_size=0.0244):
    objp = np.zeros((board_size[0]*board_size[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:board_size[0],0:board_size[1]].T.reshape(-1,2) * square_size
    objpoints, imgpoints = [], []
    
    for fname in glob.glob(f"{image_dir}/*.JPG"):
        img = cv2.imread(fname)
        ret, corners = find_chessboard_corners(img, board_size)
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

    _, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[1::-1], None, None)
    return mtx, dist, rvecs, tvecs
