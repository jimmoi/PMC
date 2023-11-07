import PersonDectecter
import PerspectiveTransform2D
import cv2
import numpy as np

# Camera
import json
from test import get_ip_camera_hik

# Constants Variables
selected_camera = 2
frame_width = 1280
frame_height = 720

# camera = cv2.VideoCapture('Dataset/B9-01.mp4')
camera = get_ip_camera_hik(selected_camera)
model = PersonDectecter.PersonDectecter(confidence_theshold=0.001)

with open(f"Dataset/Positions/camera_{selected_camera}_to_floor_plan.json", "r") as file:
    camera_position = json.load(file)
input_pts = np.float32(camera_position["camera"])  # ตำแหน่งบนกล้อง
output_pts = np.float32(camera_position["floor_plan"]) # ตำแหน่งบนแผนผังอาคาร
mapping = PerspectiveTransform2D.PerspectiveTransform2D()
mapping.fit(input_pts, output_pts)


while(True):
    # Read floor plan image data and Camera image data
    map_2d = cv2.imread("Dataset/floor1_plan_new.png")
    ret, frame = camera.read()
    
    if not ret:
        continue  # continue while ending of the video
    
    # Resize image data
    frame = cv2.resize(frame, (frame_width, frame_height))
    map_2d = cv2.resize(map_2d, (frame_width, frame_height))
    
    frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = model.dectect(frame_RGB)

    # Plot circle on camera and floor plan
    for row in res.values:
        xcenter, ycenter, width, height = row
        x = int(xcenter)
        y = int(ycenter+height/2)
        x_2d, y_2d = mapping.transform([x, y])
        cv2.circle(frame, (x, y), 10, [0, 0, 255], -1)
        cv2.circle(map_2d, (x_2d, y_2d), 3, [0, 0, 255], -1)

    # Resize for display
    window_width = 1980
    window_height = 1080
    frame = cv2.resize(frame, (window_width//2, window_height//2))
    map_2d = cv2.resize(map_2d, (window_width//2, window_height//2))
    new_window = cv2.hconcat([frame, map_2d])
    cv2.imshow('new window', new_window)

    if cv2.waitKey(1) == ord('q'):
        break
