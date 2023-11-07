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
from myutils.position import transform_camera_to_map

if __name__ == "__main__":
    # Constants
    frame_width = 1280
    frame_height = 720
    selected_camera = 2
    NUM_COLOR_CHANEL = 3

    camera = get_ip_camera_hik(2)
    # camera = cv2.VideoCapture("Dataset/B9-01.mp4")
    map_2d = cv2.imread("Dataset/floor1_plan_new.png")

    # Get position and resize
    _, frame = camera.read()
    frame = cv2.resize(frame, (frame_width, frame_height))
    map_2d = cs2.resize(map_2d, (frame_width, frame_height))

    with open(f"Dataset/Positions/camera_{selected_camera}_to_floor_plan.json", "r") as file:
        camera_position = json.load(file)

    mapping = transform_camera_to_map(
        input_coordinates=camera_position["camera"],
        output_coordinates=camera_position["floor_plan"],
    )
