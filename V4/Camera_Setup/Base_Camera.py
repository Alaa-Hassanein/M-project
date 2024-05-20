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
cap = cv.VideoCapture(0)

ret, frame = cap.read()
# Undistort the frame
undistorted_frame = cv.undistort(frame, camera_matrix, distortion_coeffs)
if ret:
    # Save the captured frame as "RAW_MAP.png"
    cv.imwrite('Map_Gen/RAW_MAP.png', undistorted_frame)
    print("Image saved as RAW_MAP.png")
else:
    print("Error capturing image")

# Release the camera and close the window
cap.release()
cv.destroyAllWindows()
