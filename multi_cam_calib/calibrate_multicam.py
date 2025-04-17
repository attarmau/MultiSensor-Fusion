# Chain camera poses (e.g., Cam0 is origin, Cam1 relative to Cam0, Cam2 relative to Cam1...)
def compute_global_poses(relative_poses):
    global_poses = {0: (np.eye(3), np.zeros((3,1)))}
    for cam_id, (R, T) in relative_poses.items():
        R_prev, T_prev = global_poses[cam_id - 1]
        R_global = R @ R_prev
        T_global = R @ T_prev + T
        global_poses[cam_id] = (R_global, T_global)
    return global_poses
