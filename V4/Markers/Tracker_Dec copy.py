

import math
import csv
import pandas as pd
import cv2
import numpy as np
from PIL import Image
import csv
import os


# Read the CSV file into a pandas DataFrame
df = pd.read_csv('V4/Map_Gen/aruco_markers.csv')

class Marker:
    def __init__(self, ID, center_x, center_y, height, width, angle_degrees,Top_Left_X,Top_Left_Y,Top_Right_X,Top_Right_Y,Bottom_Left_X,Bottom_Left_Y,Bottom_Right_X,Bottom_Right_Y ):
        self.ID = ID
        self.x = center_x
        self.y = center_y
        self.height = height
        self.width = width
        self.angle = angle_degrees
        self.Top_Left_X = Top_Left_X
        self.Top_Left_Y = Top_Left_Y
        self.Top_Right_X = Top_Right_X
        self.Top_Right_Y = Top_Right_Y
        self.Bottom_Left_X = Bottom_Left_X
        self.Bottom_Left_Y = Bottom_Left_Y
        self.Bottom_Right_X = Bottom_Right_X
        self.Bottom_Right_Y = Bottom_Right_Y

markers = []
for _, row in df.iterrows():
    markers.append(Marker(row['ID'], row['Center_X'], row['Center_Y'],
                          row['Height'], row['Width'], row['Angle_Degrees'],
                          row['Top_Left_X'],row['Top_Left_Y'],
                          row['Top_Right_X'],row['Top_Right_Y'],
                          row['Bottom_Left_X'],row['Bottom_Left_Y'],
                          row['Bottom_Right_X'],row['Bottom_Right_Y']))
Track1 = next((m for m in markers if m.ID == 1), None)
Track2 = next((m for m in markers if m.ID == 2), None)
Track3 = next((m for m in markers if m.ID == 32), None)
Track4 = next((m for m in markers if m.ID == 3), None)






# Load an image (replace 'your_image.jpg' with the actual image file path)
image_path = 'v4/Map_Gen/RAWMAP.png'
image = cv2.imread(image_path) # read the image capture
rows,cols,ch = image.shape
pts1 = np.float32([[Track1.Top_Right_X,Track1.Top_Right_Y],[Track2.Top_Left_X,Track2.Top_Left_Y],[Track3.Bottom_Right_X,Track3.Bottom_Right_Y],[Track4.Bottom_Left_X,Track4.Bottom_Left_Y]])
pts2 = np.float32([[0,0],[1080,0],[1080,1920],[0,1920]])
M = cv2.getPerspectiveTransform(pts1,pts2)
image = cv2.warpPerspective(image,M,(cols,rows))
#image_path = 'V4/Map_Gen/image.png'
cv2.imwrite("V4/Map_Gen/QWERTY_MAP.png",image)

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
        fieldnames = ['ID', 'Center_X', 'Center_Y', 'Height', 'Width', 'Angle_Degrees',
                      'Top_Left_X', 'Top_Left_Y', 'Top_Right_X', 'Top_Right_Y',
                      'Bottom_Left_X', 'Bottom_Left_Y', 'Bottom_Right_X', 'Bottom_Right_Y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each detected marker
        for i in range(len(ids)):
            marker_corners = corners[i][0]

            # Calculate dimensions (width and height)
            width = np.linalg.norm(marker_corners[0] - marker_corners[1])
            height = np.linalg.norm(marker_corners[1] - marker_corners[2])

            # Calculate the angle of the marker with respect to the horizontal axis
            dx = marker_corners[1][0] - marker_corners[0][0]
            dy = marker_corners[1][1] - marker_corners[0][1]
            angle_degrees = math.degrees(math.atan2(dy, dx))

            # Calculate the center (x, y) coordinates of the marker
            center_x = int(np.mean(marker_corners[:, 0]))
            center_y = int(np.mean(marker_corners[:, 1]))

            # Write marker information to the CSV file
            writer.writerow({'ID': ids[i][0], 'Center_X': center_x, 'Center_Y': center_y,
                             'Height': height, 'Width': width, 'Angle_Degrees': angle_degrees,
                             'Top_Left_X': marker_corners[0][0], 'Top_Left_Y': marker_corners[0][1],
                             'Top_Right_X': marker_corners[1][0], 'Top_Right_Y': marker_corners[1][1],
                             'Bottom_Left_X': marker_corners[2][0], 'Bottom_Left_Y': marker_corners[2][1],
                             'Bottom_Right_X': marker_corners[3][0], 'Bottom_Right_Y': marker_corners[3][1]})

    print("Marker information saved to aruco_markers.csv")

else:
    print("No ArUco markers detected in the image.")
