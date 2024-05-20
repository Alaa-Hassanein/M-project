import cv2
import numpy as np
import math

# Initialize the camera (e.g., webcam)
cap = cv2.VideoCapture(0)

# Define the ArUco dictionary and parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()
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

            # Calculate the angle of the marker with respect to the horizontal axis
            dx = corners[i][0][1][0] - corners[i][0][0][0]
            dy = corners[i][0][1][1] - corners[i][0][0][1]
            angle_degrees = math.degrees(math.atan2(dy, dx))

            # Calculate the center (x, y) coordinates of the marker
            center_x = int(np.mean(corners[i][0][:, 0]))
            center_y = int(np.mean(corners[i][0][:, 1]))

            # Draw the marker, angle, and position
            cv2.aruco.drawDetectedMarkers(frame, corners)
            cv2.putText(frame, f"ID {ids[i][0]} ({angle_degrees:.2f} deg)", (center_x, center_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(frame, f"Size: {width:.2f} x {height:.2f}", (center_x, center_y + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(frame, f"Size: {center_x:.2f} x {center_y:.2f}", (center_x, center_y + 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            #print(center_x,center_y)

    # Show the result
    cv2.imshow('ArUco Markers', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera
cap.release()
cv2.destroyAllWindows()
