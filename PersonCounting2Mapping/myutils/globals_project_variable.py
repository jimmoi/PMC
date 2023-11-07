""" 
Global variables for entire project can be access or edit

Examples:
---------
>>> from myutils import globals_project_variable as globals_variable
>>> globals_variable.THREAD_ACTIVATE_STATUS
"""

import numpy as np

# Control status of retrive camera thread in difference files
THREAD_ACTIVATE_STATUS = True

# Declare global variables for projects
NUM_COLOR_CHANEL = 3
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# Final Frame Size for display
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# Create Empty Black Screen Image
empty_frame = np.zeros(
    shape=(
        FRAME_HEIGHT,
        FRAME_WIDTH,
        NUM_COLOR_CHANEL,
    ),
    dtype="uint8",
)
