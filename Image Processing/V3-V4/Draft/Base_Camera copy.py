import cv2 as cv
import numpy as np
from cv2 import aruco
import numpy as np
marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
param_markers = aruco.DetectorParameters()
# Load the calibration data from multimatrix.npz
calibration_data = np.load('Camera_Setup/MultiMatrix.npz')
camera_matrix = calibration_data['camMatrix']
distortion_coeffs = calibration_data['distCoef']
r_vectors = calibration_data["rVector"]
t_vectors = calibration_data["tVector"]
# Initialize the camera (e.g., webcam)
cap = cv.VideoCapture("http://192.168.1.12:8080/video")
ret, frame = cap.read()
# Undistort the frame
undistorted_frame = frame #cv.undistort(frame, camera_matrix, distortion_coeffs)
if ret:
    # Save the captured frame as "RAW_MAP.png"
    cv.imwrite('Map_Gen/RAW_MAP.png', frame)
    mframe = undistorted_frame #frame#undistorted_frame
    gray_frame = cv.cvtColor(mframe, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )
    if marker_corners:
        for ids, corners in zip(marker_IDs, marker_corners):
            cv.polylines(
                mframe, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_left = corners[3].ravel()
            cv.putText(
                mframe,
                f"id: {ids[0]}",
                top_right,
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (200, 100, 0),
                2,
                cv.LINE_AA,
            )
    cv.imwrite('V4/Map_Gen/TRACK_MAP.png', mframe)
    print("Image saved as RAW_MAP.png")
else:
    print("Error capturing image")
# Release the camera and close the window
cap.release()
cv.destroyAllWindows()
