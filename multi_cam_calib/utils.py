import numpy as np

def transform_to_camera1(R, T, point_camera2):
    """
    Transform a 3D point from camera2's coordinate system to camera1's.

    Parameters:
    - R: 3x3 rotation matrix (from stereo calibration)
    - T: 3x1 translation vector (from stereo calibration)
    - point_camera2: 3D point in camera2's coordinate frame (numpy array of shape (3,) or (3,1))

    Returns:
    - point_camera1: Transformed 3D point in camera1's coordinate frame
    """
    point_camera2 = np.asarray(point_camera2).reshape(3, 1)  # Ensure correct shape
    point_camera1 = R @ point_camera2 + T
    return point_camera1.flatten()  # Return as flat array
