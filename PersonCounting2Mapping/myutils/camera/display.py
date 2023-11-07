""" Module about camera
Descriptions:
-------------
Display and Concatenate functions
"""

import cv2
from myutils import globals_project_variable as globals_variable


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
                list_frame.append(globals_variable.empty_frame)
        row_frame = hconcat_resize(list_frame)
        row_frames.append(row_frame)
    all_frame = vconcat_resize(row_frames)
    return all_frame


def display(current_frames_copy, map_2d):
    """
    Display all camera in current_frames_copy

    Parameters:
    -----------
    current_frames_copy: list
        list of a copy of current frames
    map_2d: np.array
        a floor plan frame

    Examples:
    ---------
    >>> display(current_frames_copy, map_2d)
    """
    all_frame = vhconcat_resize(current_frames_copy, max_col=3)
    all_frame_plus_minimap = hconcat_resize([all_frame, map_2d])
    all_frame_plus_minimap = cv2.resize(
        all_frame_plus_minimap, (globals_variable.WINDOW_WIDTH, globals_variable.WINDOW_HEIGHT)
    )
    cv2.imshow("All camera + minimap", all_frame_plus_minimap)
