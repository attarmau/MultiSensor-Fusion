import cv2, numpy as np

def stereo_calibrate(objpoints, imgpoints1, imgpoints2, mtx1, dist1, mtx2, dist2, image_size):
    flags = cv2.CALIB_FIX_INTRINSIC
    ret, _, _, _, _, R, T, _, _ = cv2.stereoCalibrate(
        objpoints, imgpoints1, imgpoints2, mtx1, dist1, mtx2, dist2, image_size, flags=flags)
    return R, T
