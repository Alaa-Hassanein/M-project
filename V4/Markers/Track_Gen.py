import cv2 as cv
from cv2 import aruco

marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
MARKER_SIZE = 400  # pixels

Robot_Tracker = aruco.generateImageMarker(marker_dict,4, MARKER_SIZE)
Goal_Tracker = aruco.generateImageMarker(marker_dict, 36, MARKER_SIZE)
first = aruco.generateImageMarker(marker_dict, 1, MARKER_SIZE)
second = aruco.generateImageMarker(marker_dict, 2, MARKER_SIZE)
third = aruco.generateImageMarker(marker_dict, 3, MARKER_SIZE)
fourth = aruco.generateImageMarker(marker_dict, 32, MARKER_SIZE)
# cv.imshow("img", marker_image)
cv.imwrite(f"V4/Markers/Trackers/Robot_Tracker.png", Robot_Tracker)
cv.imwrite(f"V4/Markers/Trackers/Goal_Tracker.png", Goal_Tracker)
cv.imwrite(f"V4/Markers/Trackers/first.png", first)
cv.imwrite(f"V4/Markers/Trackers/second.png", second)
cv.imwrite(f"V4/Markers/Trackers/third.png", third)
cv.imwrite(f"V4/Markers/Trackers/fourth.png", fourth)
# cv.waitKey(0)
# break