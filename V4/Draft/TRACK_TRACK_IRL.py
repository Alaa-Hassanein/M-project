import cv2
import numpy as np

# Define the ArUco dictionary and parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()


# Load the calibration data from multimatrix.npz
calibration_data = np.load('Camera_Setup/MultiMatrix.npz')
camera_matrix = calibration_data['camMatrix']
distortion_coeffs = calibration_data['distCoef']
#r_vectors = calibration_data["rVector"]
#t_vectors = calibration_data["tVector"]

# Initialize the camera (e.g., webcam)
cap = cv2.VideoCapture('http://192.168.1.12:8080/video')#cv2.VideoCapture(0)

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()
    # Undistort the frame
    frame = cv2.undistort(frame, camera_matrix, distortion_coeffs)
    if not ret:
        continue  # Skip this frame if capture fails

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        # Process each detected marker
        for i in range(len(ids)):
            # Calculate dimensions (width and height)
            width = np.linalg.norm(corners[i][0][0] - corners[i][0][1])
            height = np.linalg.norm(corners[i][0][1] - corners[i][0][2])

            # Determine orientation (N, S, W, E)
            # Based on the arrangement of corners
            if corners[i][0][0][1] < corners[i][0][2][1]:
                orientation = 'N'  # Top edge is facing upward
            else:
                orientation = 'S'  # Bottom edge is facing upward

            if corners[i][0][0][0] < corners[i][0][2][0]:
                orientation += 'E'  # Right edge is facing upward
            else:
                orientation += 'W'  # Left edge is facing upward

            # Calculate the center (x, y) coordinates of the marker
            center_x = int(np.mean(corners[i][0][:, 0]))
            center_y = int(np.mean(corners[i][0][:, 1]))

            # Draw the marker and orientation
            cv2.aruco.drawDetectedMarkers(frame, corners)
            cv2.putText(frame, f"ID {ids[i][0]} ({center_x}, {center_y})", (center_x, center_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(frame, f"Size: {width:.2f} x {height:.2f}", (center_x, center_y + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(frame, f"Orientation: {orientation}", (center_x, center_y + 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Show the result
    cv2.imshow('ArUco Markers', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera
cap.release()
cv2.destroyAllWindows()
