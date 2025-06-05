import os
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Camera intrinsics for cam1
camera_matrix1 = np.array([
    [1635.2139320584938, 0.0, 491.70552818049805],
    [0.0, 1649.261285014665, 563.1537334218066],
    [0.0, 0.0, 1.0]
])
dist_coeffs1 = np.array([
    -0.7783523102247556,
    0.805830549333204,
    -0.0010772652725541043,
    -0.023382106177638144,
    5.428755128684437
])

# Camera intrinsics for cam2 (replace with your actual values)
camera_matrix2 = np.array([
    [1600.0, 0.0, 500.0],
    [0.0, 1600.0, 550.0],
    [0.0, 0.0, 1.0]
])
dist_coeffs2 = np.array([
    -0.7, 0.8, -0.001, -0.02, 5.4
])

# Directories
input_dir_cam1 = '/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/intrinsic/cam1'
input_dir_cam2 = '/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/intrinsic/cam2'
output_dir = '/Users/judyhuang/Downloads/MultiSensor-Fusion-main/data/intrinsic/comparisons_combined'
os.makedirs(output_dir, exist_ok=True)

# Get sorted image filenames for cam1
image_paths_cam1 = sorted(glob.glob(os.path.join(input_dir_cam1, '*.jpg')))
image_paths_cam2 = sorted(glob.glob(os.path.join(input_dir_cam2, '*.jpg')))

# Make sure both lists are aligned by index (assuming same names)
for i in range(len(image_paths_cam1)):
    image_path_cam1 = image_paths_cam1[i]
    filename_cam1 = os.path.basename(image_path_cam1)

    # Find corresponding cam2 image
    image_path_cam2 = os.path.join(input_dir_cam2, filename_cam1)
    if not os.path.exists(image_path_cam2):
        print(f"[WARNING] No matching cam2 image for: {filename_cam1}")
        continue

    # Load images
    img1 = cv2.imread(image_path_cam1)
    img2 = cv2.imread(image_path_cam2)

    if img1 is None or img2 is None:
        print(f"[ERROR] Could not load image pair: {filename_cam1}")
        continue

    # Convert to RGB
    img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

    # Undistort cam1
    h1, w1 = img1.shape[:2]
    new_camera_matrix1, roi1 = cv2.getOptimalNewCameraMatrix(
        camera_matrix1, dist_coeffs1, (w1, h1), 1, (w1, h1)
    )
    undistorted1 = cv2.undistort(img1, camera_matrix1, dist_coeffs1, None, new_camera_matrix1)
    undistorted1_rgb = cv2.cvtColor(undistorted1, cv2.COLOR_BGR2RGB)

    # Undistort cam2
    h2, w2 = img2.shape[:2]
    new_camera_matrix2, roi2 = cv2.getOptimalNewCameraMatrix(
        camera_matrix2, dist_coeffs2, (w2, h2), 1, (w2, h2)
    )
    undistorted2 = cv2.undistort(img2, camera_matrix2, dist_coeffs2, None, new_camera_matrix2)
    undistorted2_rgb = cv2.cvtColor(undistorted2, cv2.COLOR_BGR2RGB)

    # Plot 2x2 grid
    fig, axs = plt.subplots(2, 2, figsize=(14, 12))
    axs[0, 0].imshow(img1_rgb)
    axs[0, 0].set_title("Cam1 - Original")
    axs[0, 0].axis('off')

    axs[0, 1].imshow(undistorted1_rgb)
    axs[0, 1].set_title("Cam1 - Undistorted")
    axs[0, 1].axis('off')

    axs[1, 0].imshow(img2_rgb)
    axs[1, 0].set_title("Cam2 - Original")
    axs[1, 0].axis('off')

    axs[1, 1].imshow(undistorted2_rgb)
    axs[1, 1].set_title("Cam2 - Undistorted")
    axs[1, 1].axis('off')

    plt.tight_layout()

    # Save figure
    filename_no_ext = os.path.splitext(filename_cam1)[0]
    save_path = os.path.join(output_dir, f'{filename_no_ext}_comparison_combined.jpg')
    plt.savefig(save_path)
    plt.close()

    print(f"[INFO] Saved comparison image: {save_path}")
