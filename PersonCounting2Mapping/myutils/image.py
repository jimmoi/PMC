# importing the module
import cv2
from copy import copy


def get_coordinates(img):
    coordinates = []
    img = copy(img) # copy the image data to new allocated memory locations

    def click_event(event, x, y, flags, params):
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
            # displaying the coordinates
            # on the Shell
            print(x, " ", y)

            # displaying the coordinates
            # on the image window
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.circle(img, (x, y), 10, [255, 255, 0], 1)
            cv2.putText(img, str(x) + "," + str(y), (x, y), font, 1, (100, 100, 255), 2)
            cv2.imshow("Drawing points", img)
            coordinates.append([x, y])

        # checking for right mouse clicks
        if event == cv2.EVENT_RBUTTONDOWN:
            # displaying the coordinates
            # on the Shell
            print(x, " ", y)

            # displaying the coordinates
            # on the image window
            font = cv2.FONT_HERSHEY_SIMPLEX
            b = img[y, x, 0]
            g = img[y, x, 1]
            r = img[y, x, 2]
            cv2.putText(
                img,
                str(b) + "," + str(g) + "," + str(r),
                (x, y),
                font,
                1,
                (255, 255, 0),
                2,
            )
            cv2.imshow("Drawing points", img)

    cv2.imshow("Drawing points", img)
    cv2.setMouseCallback("Drawing points", click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return coordinates


def rescale_frame(frame, percent=50):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


def rescale_frame_restore(frame, percent=150):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


""" Example
if __name__=="__main__":

	# reading the image
	img = cv2.imread('lena.jpg', 1)

	# displaying the image
	cv2.imshow('image', img)

	# setting mouse handler for the image
	# and calling the click_event() function
	cv2.setMouseCallback('image', click_event)

	# wait for a key to be pressed to exit
	cv2.waitKey(0)

	# close the window
	cv2.destroyAllWindows()
"""
