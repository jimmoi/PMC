# ============= Requiring Module =============
import cv2 as cv
from utils.image import (get_coordinates,
                         rescale_frame,
                         rescale_frame_restore)

# ============= Getting file locations =============
img_path = "Dataset/floor1.png"
img_plan_path = "Dataset/floor1_plan.png"


# ============= Load images =============
img = cv.imread(img_path)
img_floor = cv.imread(img_plan_path)

# ============= Sample position coordinates data =============
cv.circle(img=img, center=(1360, 800), radius=20, color=[100, 100, 255], thickness=-1)
cv.circle(img=img, center=(1430, 400), radius=20, color=[100, 100, 255], thickness=-1)

img = rescale_frame(img)

# ============= Input Image =============
# get_coordinates(img)
cv.circle(img=img, center=(632, 62), radius=10, color=[255, 255, 255], thickness=-1)
cv.circle(img=img, center=(770, 62), radius=10, color=[255, 255, 255], thickness=-1)
cv.circle(img=img, center=(414, 812), radius=10, color=[255, 255, 255], thickness=-1)
cv.circle(img=img, center=(980, 812), radius=10, color=[255, 255, 255], thickness=-1)
# img = rescale_frame_restore(img)

cv.imshow("Frame", img)

# ============= Output Image =============
# get_coordinates(img)
cv.circle(img=img_floor, center=(468, 363), radius=5, color=[100, 100, 255], thickness=-1)
cv.circle(img=img_floor, center=(512, 363), radius=5, color=[100, 100, 255], thickness=-1)
cv.circle(img=img_floor, center=(469, 565), radius=5, color=[100, 100, 255], thickness=-1)
cv.circle(img=img_floor, center=(510, 565), radius=5, color=[100, 100, 255], thickness=-1)
img_floor = rescale_frame(img_floor, 80)
cv.imshow("Floor Plan", img_floor)

# ============= Destroy Program =============
cv.waitKey(0)
cv.destroyAllWindows()

