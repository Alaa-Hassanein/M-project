import cv2
import numpy as np
import math
import csv

# Load an image (replace 'your_image.jpg' with the actual image file path)
image_path = 'Map_Gen/RAW_MAP.png'
image_path = 'V4/Data/MAPPPPPP.png'
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Define the ArUco dictionary and parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

# Detect markers
corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

if ids is not None:
    # Create a CSV file to store marker information
    with open('V4/Map_Gen/aruco_markers.csv', 'w', newline='') as csvfile:
        fieldnames = ['ID', 'Center_X', 'Center_Y', 'Height', 'Width', 'Angle_Degrees']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

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

            # Write marker information to the CSV file
            writer.writerow({'ID': ids[i][0], 'Center_X': center_x, 'Center_Y': center_y,
                             'Height': height, 'Width': width, 'Angle_Degrees': angle_degrees})

    print("Marker information saved to aruco_markers.csv")

else:
    print("No ArUco markers detected in the image.")

# Display the result
#cv2.imshow('ArUco Markers', image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
