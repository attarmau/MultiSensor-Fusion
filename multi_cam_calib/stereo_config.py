import json
import numpy as np
from utils import transform_to_camera1

# Load extrinsic parameters from stereo_config.json
with open('camera_calibration/stereo_config.json', 'r') as f:
    data = json.load(f)

R = np.array(data['R'], dtype=np.float32)
T = np.array(data['T'], dtype=np.float32)

# Now, you can use the transform_to_camera1 function
point_camera2 = np.array([1.0, 2.0, 3.0])  # Example 3D point in camera2's coordinate system
point_camera1 = transform_to_camera1(R, T, point_camera2)

print("Transformed point in camera1's coordinate system:", point_camera1)
