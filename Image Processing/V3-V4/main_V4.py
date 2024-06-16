import runpy
import cv2
cap = cv2.VideoCapture('http://192.168.1.12:8080/video')
_, frame = cap.read()
cap.release()
cv2.imwrite("V4/Map_Gen/RAW_MAP.png", frame)
#runpy.run_path(path_name='V4/Camera_Setup/Base_Camera.py')
runpy.run_path(path_name='V4/Markers/Tracker_Dec.py')
runpy.run_path(path_name='V4/Markers/Tracker_Dec copy.py')
runpy.run_path(path_name='V4/Markers/Tracker_Dec copy 2.py')
runpy.run_path(path_name='V4/Markers/Tracker_Dec copy 3.py')
runpy.run_path(path_name='V4/Map_Gen/MAP.py')