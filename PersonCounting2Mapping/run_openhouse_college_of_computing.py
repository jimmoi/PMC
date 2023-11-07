""" Grand Opening College of Computing Khon Kaen University

Descriptions:
-------------
    Dectect person from camera and show people locations on floor plan map

Examples:
---------
    $ python run_grand_opening_college_of_computing_new.py

Contributors:
-------------
    - https://github.com/chonsawat
    - https://github.com/nithan-git
    - https://github.com/FrongTH
"""
import threading
from copy import deepcopy

import cv2
import numpy as np
import matplotlib.pyplot as plt

from myutils import transform, heatmap
from myutils import PersonDectecter
from myutils.camera import display, camera
from myutils.camera.settings import selected_cameras
from myutils.crop import crop_grand_opening as crop
from myutils import globals_project_variable as globals_variable


def main():
    """
    This function is doing
    - Retrive camera(s)
    - Detect people
    - Draw Regtangle on area that will not detect people
    - this function will handle `redefined-outer-name`
        - `redefined-inner-name` is ambiguous between global and local variables scope
    """

    cameras = [camera.get_ip_camera_hik(num_camera) for num_camera in selected_cameras]
    current_frames = [globals_variable.empty_frame] * len(cameras)
    model = PersonDectecter.PersonDectecter(confidence_theshold=0)

    # Run thread
    for index_camera in range(len(cameras)):
        receive_thread = threading.Thread(
            target=camera.receive,
            args=(cameras, current_frames, index_camera),
        )
        receive_thread.start()

    # Load the coordinates for perspective ranform and keep into the list
    list_mapping = transform.get_transform_for_college_of_computing_floor_map(selected_cameras)

    # Crop and map transform
    map_2d_template = cv2.imread("Dataset/floor1_plan_new.png")
    map_2d_template = cv2.resize(
        map_2d_template, (globals_variable.FRAME_WIDTH, globals_variable.FRAME_HEIGHT)
    )
    while True:
        coordinates = []
        map_2d = map_2d_template.copy()  # Clear Image Data
        current_frames_copy = deepcopy(current_frames)
        for num_camera, current_frame in enumerate(current_frames_copy):
            mapping = list_mapping[num_camera]

            # Crop image manually for grand opening day
            if num_camera in (3, 5):
                crop.crop_image_manual(
                    num_camera,
                    current_frame,
                )

            frame_rgb = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
            result = model.dectect(frame_rgb)

            # Drawn a Retangle into specific camera to told there will not detect person on display
            if num_camera in (3, 5):
                crop.draw_rectangle(num_camera, current_frame, current_frames)

            # Transform to floor plan map
            """
            >>> result.values
                list of [xcenter, ycenter, width, height]
            >>> x = int(xcenter)
            >>> y = int(ycenter + height / 2)
            >>> x_minimap, y_minimap = mapping.transform([x, y])
                position on map
            """
            
            for row in result.values:
                transform.tranform_to_floor(
                    row=row, mapping=mapping, current_frame=current_frame, map_2d=map_2d,
                    coordinates=coordinates
                )
                
        heatmap_img = heatmap.im_kde(coordinates)
        heatmap_img = heatmap.overay_heatmap(map_2d, heatmap_img)
        map_2d = heatmap_img

        # Display all camera
        display.display(current_frames_copy, map_2d)

        # Exit the program
        if cv2.waitKey(1) == ord("q") or cv2.waitKey(1) == ord("ๆ"):
            globals_variable.THREAD_ACTIVATE_STATUS = False
            break

    # Release camera & destroy frame
    cv2.destroyAllWindows()


# When run this file do:
if __name__ == "__main__":
    main()
