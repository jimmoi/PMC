""" 
Functions for grand opening to Manual crop and draw rectangle area

Examples:
---------
>>> from myutils.crop import crop_grand_opening as crop
>>> crop.crop_image_manual(
                    num_camera,
                    current_frame,
                )
"""

import cv2
import numpy as np
from myutils import globals_project_variable as globals_variable


def crop_image_manual(num_camera, current_frame):
    """
    Crop a image for each camera
    
    Parameters:
    -----------
    num_camera : int
        a index of camera that will be cropped
    current_frame : np.array
        a frame of camera that you read to detect people

    Examples:
    ---------
    >>> crop_image_manual(
            3,
            current_frame,
        )
    """
    if num_camera == 3:
        current_frame[:, 790:] = np.zeros(
            shape=(
                globals_variable.FRAME_HEIGHT,
                globals_variable.FRAME_WIDTH - 790,
                globals_variable.NUM_COLOR_CHANEL,
            ),
            dtype="uint8",
        )
        # cv2.imshow("Camera 6", current_frame)
    if num_camera == 5:
        current_frame[:250, :] = np.zeros(
            shape=(250, globals_variable.FRAME_WIDTH, globals_variable.NUM_COLOR_CHANEL),
            dtype="uint8",
        )
        current_frame[:, 1120:] = np.zeros(
            shape=(
                globals_variable.FRAME_HEIGHT,
                globals_variable.FRAME_WIDTH - 1120,
                globals_variable.NUM_COLOR_CHANEL,
            ),
            dtype="uint8",
        )
        # cv2.imshow("crop camera 9", current_frame)


def draw_rectangle(num_camera, current_frame, current_frames):
    """
    Draw a rectangle on area that you do not need to detect people
    
    Paremeters:
    -----------
    num_camera: int
        a no. of index camera in `selected_cameras`
    current_frame: np.array
        a frame that come from camera
    current_frames: np.array
        list of a frame that come from camera
    
    Examples:
    ---------
    >>> crop.draw_rectangle(3, current_frame, current_frames)
    """
    if num_camera == 3:
        current_frame[:, :] = current_frames[num_camera]
        cv2.rectangle(
            current_frame,
            (790, 0),
            (globals_variable.FRAME_WIDTH, globals_variable.FRAME_HEIGHT),
            (0, 0, 0),
            5,
        )
    if num_camera == 5:
        current_frame[:, :] = current_frames[num_camera]
        cv2.rectangle(current_frame, (0, 0), (globals_variable.FRAME_WIDTH, 250), (0, 0, 0), 20)
        cv2.rectangle(
            current_frame,
            (1120, 0),
            (globals_variable.FRAME_WIDTH, globals_variable.FRAME_HEIGHT),
            (0, 0, 0),
            5,
        )
