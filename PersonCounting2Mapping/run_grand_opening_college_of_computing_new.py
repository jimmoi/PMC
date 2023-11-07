import threading
from copy import deepcopy
import cv2
import numpy as np
from myutils import transform, heatmap, PersonDectecter
from myutils.camera import display, camera
from myutils.camera.settings import selected_cameras
from myutils.crop import crop_grand_opening as crop
from myutils import globals_project_variable as globals_variable

def main():
    cameras = [camera.get_ip_camera_hik(num) for num in selected_cameras]
    frames = [globals_variable.empty_frame] * len(cameras)
    model = PersonDectecter.PersonDectecter(confidence_theshold=0)
    list_mapping = transform.get_transform_for_college_of_computing_floor_map(selected_cameras)
    map_2d_template = cv2.imread("Dataset/floor1_plan_new.png")
    map_2d_template = cv2.resize(map_2d_template, (globals_variable.FRAME_WIDTH, globals_variable.FRAME_HEIGHT))

    for index_camera in range(len(cameras)):
        receive_thread = threading.Thread(
            target=camera.receive,
            args=(cameras, frames, index_camera),
        )
        receive_thread.start()

    while True:
        coordinates = []
        map_2d = map_2d_template.copy()
        frames_copy = deepcopy(frames)

        for num, frame in enumerate(frames_copy):
            mapping = list_mapping[num]
            if num in (3, 5):
                crop.crop_image_manual(num, frame)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = model.dectect(frame_rgb)
            if num in (3, 5):
                crop.draw_rectangle(num, frame, frames)

            for row in result.values:
                transform.tranform_to_floor(row=row, mapping=mapping, current_frame=frame, map_2d=map_2d, coordinates=coordinates)

        heatmap_img = heatmap.im_kde(coordinates)
        heatmap_img = heatmap.overay_heatmap(map_2d, heatmap_img)
        map_2d = heatmap_img
        display.display(frames_copy, map_2d)

        if cv2.waitKey(1) in (ord("q"), ord("ๆ")):
            globals_variable.THREAD_ACTIVATE_STATUS = False
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()