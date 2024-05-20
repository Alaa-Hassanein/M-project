import cv2 as cv
from cv2 import aruco

marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
MARKER_SIZE = 400  # pixels

Robot_Tracker = aruco.generateImageMarker(marker_dict, 4, MARKER_SIZE)
Goal_Tracker = aruco.generateImageMarker(marker_dict, 36, MARKER_SIZE)

# cv.imshow("img", marker_image)
cv.imwrite(f"Markers/Trackers/Robot_Tracker.png", Robot_Tracker)
cv.imwrite(f"Markers/Trackers/Goal_Tracker.png", Goal_Tracker)
# cv.waitKey(0)
# break