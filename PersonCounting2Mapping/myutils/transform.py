""" 
This Module is keep method to use for transform position    
"""

import json

import cv2
import numpy as np
from myutils import PerspectiveTransform2D

''' TODO: Wait for delete
def transform_camera_to_map(input_coordinates: list, output_coordinates: list):
    """
    Transform position on camera to floop map position
    
    Parameters:
    -----------
    input_coordinates: list
        list of coordinates to transform position on camera positions
    output_coordinates: list
        list of coordinates to transform position on floor map positions
        
    Return:
    -------
    mapping:
        use for mapping from camera coordinates to floor map coordinates
        
    Examples:
    ---------
    >>> mapping = transform_camera_to_map(input_coordinates=camera_position["camera"], output_coordinates=camera_position["floor_plan"])
    """
    input_pts = np.float32(input_coordinates)  # ตำแหน่งบนกล้อง
    output_pts = np.float32(output_coordinates)  # ตำแหน่งบนแผนผังอาคาร
    mapping = PerspectiveTransform2D.PerspectiveTransform2D()
    mapping.fit(input_pts, output_pts)
    return mapping
'''


def tranform_to_floor(row, mapping, current_frame, map_2d, coordinates):
    """
    Transform a given camera position to a floor plan position
    
    Parameters:
    -----------
    row: np.array
        a prediction position from YoloV5
    mapping: list
        list from PerspectiveTransform2D models
    current_frame: np.array
        a current frame from camera
    map_2d: np.array
        a current frame of map
    
    Examples:
    ---------
    >>> transform.tranform_to_floor(
            row=row, mapping=mapping, current_frame=current_frame, map_2d=map_2d
        )
    """
    xcenter, ycenter, width, height = row
    x = int(xcenter)
    y = int(ycenter + height / 2)
    x_minimap, y_minimap = mapping.transform([x, y])
    coordinates.append([x_minimap, y_minimap])
    
    # People
    cv2.circle(current_frame, (x, y), 10, [0, 0, 255], -1)
    cv2.rectangle(current_frame, (x-int(width)//2, y), (x+int(width), y-int(height)), (0, 100, 255), 10)

    # Map
    ## Coordinates start on top-left corner at (0,0) or (col, row)
    cv2.circle(map_2d, (x_minimap, y_minimap), 5, [0, 0, 255], -1)


def get_transform_for_college_of_computing_floor_map(selected_cameras):
    """
    Read position of each camera from json files and convert them to PerspectiveTransform2D model
    
    Parameters:
    -----------
    selected_cameras: list
        list of all selected cameras
    
    Examples:
    ---------
    >>> list_mapping = transform.get_transform_for_college_of_computing_floor_map(selected_cameras)
    """
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
    return list_mapping
