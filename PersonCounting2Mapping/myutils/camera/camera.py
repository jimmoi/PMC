"""
My camera utils module for get camera data
"""

import cv2
from myutils.camera.settings import username, password, ip
from myutils import globals_project_variable as globals_variable


def get_ip_camera_hik(num_camera: int):
    """Get camera object

    Get camera object from HIK ip camera, must be connected to KKU VPN connection

    Parameters:
    -----------
    num_camera : int
        the no. of ip camera

    Returns:
    --------
    camera: cv2.VideoCapture.open
        A camera connection for camera.read()

    Examples:
    --------
    >>> get_ip_camera_hik(2)
    """
    camera = cv2.VideoCapture()
    camera.open(f"rtsp://{username}:{password}@{ip}.{num_camera}/Streaming/channels/2")
    # camera.set(3, FRAME_WIDTH)
    # camera.set(4, FRAME_HEIGHT)
    return camera


def receive(cameras, current_frames, index_camera):
    """Get the data from the camera

    Get the data from the camera and save into `current_frames` in global variables.

    Parameters:
    -----------
    cameras : list
        list of video cameras
    current_frames : list
        list of current frames
    index_camera : int
        the no. of camera you need

    Examples:
    --------
    >>> receive_thread(cameras, current_frames, index_camera)
    """
    print(f"start receive {index_camera}")
    camera = cameras[index_camera]
    while globals_variable.THREAD_ACTIVATE_STATUS:
        ret, frame = camera.read()
        if not ret:
            continue
        frame_resize = cv2.resize(
            frame, (globals_variable.FRAME_WIDTH, globals_variable.FRAME_HEIGHT)
        )
        current_frames[index_camera] = frame_resize

    camera.release()
    print(f"Cancle Retreive : {index_camera} ...")
