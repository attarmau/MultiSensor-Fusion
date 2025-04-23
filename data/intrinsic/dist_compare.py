import cv2
import numpy as np
import matplotlib.pyplot as plt

camera_matrix = np.array([
    [1635.2139320584938, 0.0, 491.70552818049805],
    [0.0, 1649.261285014665, 563.1537334218066],
    [0.0, 0.0, 1.0]
])

dist_coeffs = np.array([
    -0.7783523102247556,
    0.805830549333204,
    -0.0010772652725541043,
    -0.023382106177638144,
    5.428755128684437
])

image_path = '/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/cam1/img_001.jpg'

image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError(f"no image：{image_path}")

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.imshow(image_rgb)
plt.title("original image")
plt.axis('off')
plt.show()

h, w = image.shape[:2]
new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
    camera_matrix, dist_coeffs, (w, h), 1, (w, h)
)

undistorted = cv2.undistort(image, camera_matrix, dist_coeffs, None, new_camera_matrix)
undistorted_rgb = cv2.cvtColor(undistorted, cv2.COLOR_BGR2RGB)

fig, axs = plt.subplots(1, 2, figsize=(14, 6))
axs[0].imshow(image_rgb)
axs[0].set_title("original image")
axs[0].axis('off')

axs[1].imshow(undistorted_rgb)
axs[1].set_title("distortion image")
axs[1].axis('off')

plt.tight_layout()
plt.show()
