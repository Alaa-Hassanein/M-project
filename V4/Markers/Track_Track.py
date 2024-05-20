import cv2
import numpy as np

# Load an image containing ArUco markers (replace with your own image)
image_path = 'Map_Gen/RAW_MAP.png'
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Define the ArUco dictionary and parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

# Detect markers
corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

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

    # Draw the marker and orientation
    cv2.aruco.drawDetectedMarkers(image, corners)
    cv2.putText(image, f"ID {ids[i][0]}", (int(corners[i][0][0][0]), int(corners[i][0][0][1])),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.putText(image, f"Size: {width:.2f} x {height:.2f}", (int(corners[i][0][0][0]), int(corners[i][0][0][1] + 20)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.putText(image, f"Orientation: {orientation}", (int(corners[i][0][0][0]), int(corners[i][0][0][1] + 40)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# Show the result
cv2.imshow('ArUco Markers', image)
cv2.waitKey(0)
cv2.destroyAllWindows()