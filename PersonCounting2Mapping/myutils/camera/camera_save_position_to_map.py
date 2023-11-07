import PersonDectecter
import PerspectiveTransform2D
import cv2
import numpy as np

# Camera
from settings import *
from test import get_ip_camera_hik

# Image position
import json
from myutils.image import get_coordinates


if __name__ == "__main__":
    # Constants
    frame_width = 1280
    frame_height = 720
    selected_camera = 8 # ["2", "4", "5", "6", "8", "9", "14"]
    NUM_COLOR_CHANEL = 3

    camera = get_ip_camera_hik(selected_camera)
    # camera = cv2.VideoCapture("Dataset/B9-01.mp4")
    map_2d = cv2.imread("Dataset/floor1_plan_new.png")
    # model = PersonDectecter.PersonDectecter(confidence_theshold=0.001)

    # Get position and resize
    _, frame = camera.read()
    frame = cv2.resize(frame, (frame_width, frame_height))
    map_2d = cv2.resize(map_2d, (frame_width, frame_height))
    
    input_coordinates = get_coordinates(frame)
    output_coordinates = get_coordinates(map_2d)
    transform_coordinate_json = {
        "name": f"Camera {selected_camera}",
        "size": {"width": frame_width, "height": frame_height},
        "camera": input_coordinates,
        "floor_plan": output_coordinates,
    }
    
    print("Input:", input_coordinates)
    print("Output:", output_coordinates)

    # Save position for transform to file
    with open(
        f"Dataset/Positions/camera_{selected_camera}_to_floor_plan.json", "w"
    ) as file:
        json.dump(transform_coordinate_json, file, indent=4)

    # Save image to `Dataset/Camera/...`
    cv2.imwrite(f"Dataset/Camera/Camera_{selected_camera}.png", frame)

    print(transform_coordinate_json)
