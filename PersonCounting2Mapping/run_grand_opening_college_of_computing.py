""" Grand Opening College of Computing Khon Kaen University

Descriptions:
-------------
    Dectect person from camera and show people locations on floor plan map

Examples:
---------
    $ python run_grand_opening_college_of_computing.py

Contributors:
-------------
    - https://github.com/chonsawat
    - https://github.com/nithan-git
    - https://github.com/FrongTH
"""
import json
import threading
from copy import deepcopy

import cv2
import numpy as np

from myutils.camera.settings import (username,
                                     password,
                                     ip,
                                     selected_cameras)
from myutils import PersonDectecter
from myutils import PerspectiveTransform2D


THREAD_ACTIVATE_STATUS = True

NUM_COLOR_CHANEL = 3
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
empty_frame = np.zeros(
    shape=(FRAME_HEIGHT, FRAME_WIDTH, NUM_COLOR_CHANEL), dtype="uint8"
)  # Create Empty Black Screen Image


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
    while THREAD_ACTIVATE_STATUS:
        ret, frame = camera.read()
        if not ret:
            continue
        frame_resize = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        current_frames[index_camera] = frame_resize


def vconcat_resize(img_list, interpolation=cv2.INTER_CUBIC):
    """Resize and Concatenate images with Vertical Alignment

    Refference:
    -----------
    https://www.geeksforgeeks.org/concatenate-images-using-opencv-in-python/
    """
    w_min = min(img.shape[1] for img in img_list)
    im_list_resize = [
        cv2.resize(
            img,
            (w_min, int(img.shape[0] * w_min / img.shape[1])),
            interpolation=interpolation,
        )
        for img in img_list
    ]
    return cv2.vconcat(im_list_resize)


def hconcat_resize(img_list, interpolation=cv2.INTER_CUBIC):
    """Resize and Concatenate images with Horizontal Alignment

    Refference:
    -----------
    https://www.geeksforgeeks.org/concatenate-images-using-opencv-in-python/
    """
    h_min = min(img.shape[0] for img in img_list)
    im_list_resize = [
        cv2.resize(
            img,
            (int(img.shape[1] * h_min / img.shape[0]), h_min),
            interpolation=interpolation,
        )
        for img in img_list
    ]
    return cv2.hconcat(im_list_resize)


def vhconcat_resize(img_list, max_col):
    """Concatenate a list of images list to display.
    Descriptions:
    -------------
    img_list: list
        list of images list
    max_col: int
        Number of columns to display
        
    Returns:
    --------
    all_frame: cv2.Frame
        Frame to display
    
    Examples:
    ---------
    >>> all_frame = vhconcat_resize(current_frames_copy, max_col=3)
    """
    if len(img_list) <= 0:
        raise Exception("vhconcat_resize img_list size wrong")
    size = len(img_list)
    row_frames = []
    for start_index in range(0, size, max_col):
        list_frame = img_list[start_index : start_index + max_col]
        size_list_frame = len(list_frame)
        if size_list_frame < 3:
            for _ in range(3 - size_list_frame):
                list_frame.append(empty_frame)
        row_frame = hconcat_resize(list_frame)
        row_frames.append(row_frame)
    all_frame = vconcat_resize(row_frames)
    return all_frame


# When run this file do:
if __name__ == "__main__":
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080

    cameras = [get_ip_camera_hik(num_camera) for num_camera in selected_cameras]
    current_frames = [empty_frame] * len(cameras)
    model = PersonDectecter.PersonDectecter(confidence_theshold=0)
    
    # Run thread
    for index_camera in range(len(cameras)):
        receive_thread = threading.Thread(
            target=receive, args=(cameras, current_frames, index_camera)
        )
        receive_thread.start()
    
    # Load the coordinates for perspective ranform and keep into the list
    list_mapping = []
    for num_camera in selected_cameras:
        with open(
            f"Dataset/Positions/camera_{num_camera}_to_floor_plan.json",
            mode="r",
            encoding="utf-8",
        ) as file:
            camera_position = json.load(file)
            input_pts = np.float32(camera_position["camera"])
            output_pts = np.float32(camera_position["floor_plan"])
            mapping = PerspectiveTransform2D.PerspectiveTransform2D()
            mapping.fit(input_pts, output_pts)
            list_mapping.append(mapping)

    map_2d_template = cv2.imread("Dataset/floor1_plan_new.png")
    map_2d_template = cv2.resize(map_2d_template, (FRAME_WIDTH, FRAME_HEIGHT))
    while True:
        map_2d = map_2d_template.copy()  # Clear Image Data

        # Start dectect and tranform
        current_frames_copy = deepcopy(current_frames)
        for num_camera, current_frame in enumerate(current_frames_copy):
            mapping = list_mapping[num_camera]

            # ======  Crop image manually ======
            if num_camera == 3:
                current_frame[:, 790:] = np.zeros(
                    shape=(FRAME_HEIGHT, FRAME_WIDTH - 790, NUM_COLOR_CHANEL),
                    dtype="uint8",
                )
                # cv2.imshow("Camera 6", current_frame)
            if num_camera == 5:
                current_frame[:250, :] = np.zeros(
                    shape=(250, FRAME_WIDTH, NUM_COLOR_CHANEL), dtype="uint8"
                )
                current_frame[:, 1120:] = np.zeros(
                    shape=(FRAME_HEIGHT, FRAME_WIDTH - 1120, NUM_COLOR_CHANEL),
                    dtype="uint8",
                )
                # cv2.imshow("crop camera 9", current_frame)

            frame_RGB = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
            result = model.dectect(frame_RGB)

            # Drawn a Retangle into specific camera to told there will not detect person on display
            # Retangle means: it can be detect person from another camera
            if num_camera == 3:
                current_frame[:, :] = current_frames[num_camera]
                cv2.rectangle(
                    current_frame, (790, 0), (FRAME_WIDTH, FRAME_HEIGHT), (0, 0, 0), 5
                )
            if num_camera == 5:
                current_frame[:, :] = current_frames[num_camera]
                cv2.rectangle(current_frame, (0, 0), (FRAME_WIDTH, 250), (0, 0, 0), 20)
                cv2.rectangle(
                    current_frame, (1120, 0), (FRAME_WIDTH, FRAME_HEIGHT), (0, 0, 0), 5
                )


            # Transform to floor plan map
            for row in result.values:
                xcenter, ycenter, width, height = row
                x = int(xcenter)
                y = int(ycenter + height / 2)
                x_minimap, y_minimap = mapping.transform([x, y])
                cv2.circle(current_frame, (x, y), 10, [0, 0, 255], -1)
                cv2.circle(map_2d, (x_minimap, y_minimap), 5, [0, 0, 255], -1)

        # Display all camera
        all_frame = vhconcat_resize(current_frames_copy, max_col=3)
        all_frame_plus_minimap = hconcat_resize([all_frame, map_2d])
        all_frame_plus_minimap = cv2.resize(
            all_frame_plus_minimap, (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        cv2.imshow("All camera + minimap", all_frame_plus_minimap)

        # Exit the program
        if cv2.waitKey(1) == ord("q"):
            THREAD_ACTIVATE_STATUS = False
            break
