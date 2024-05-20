import pandas as pd
import cv2
import numpy as np
from PIL import Image
import csv
import os

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('Map_Gen/aruco_markers.csv')
# Define the Marker class
class Marker:
    def __init__(self, ID, center_x, center_y, height, width, angle_degrees):
        self.ID = ID
        self.x = center_x
        self.y = center_y
        self.height = height
        self.width = width
        self.angle = angle_degrees
def process_image(image, hsv_filter, edge_detection):
  if len(image.shape) == 2:  # Grayscale image
      image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
  elif image.shape[2] != 3:  # Non-BGR color format
      image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

  # Color filtering based on HSV values
  lower_hsv = np.array(hsv_filter[0])
  upper_hsv = np.array(hsv_filter[1])
  hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # Convert to HSV color space
  mask = cv2.inRange(hsv_img, lower_hsv, upper_hsv)  # Create mask for the HSV range
  image = cv2.bitwise_and(image, image, mask=mask)  # Apply mask

  # Edge detection (using Sobel filter)
  if edge_detection:
      gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
      sobelx = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=5)  # Sobel filter for horizontal edges
      sobely = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=5)  # Sobel filter for vertical edges
      edges = cv2.bitwise_or(sobelx, sobely)  # Combine horizontal and vertical edges
      image = edges  # Replace original image with edge detection result

  return image
def save_processed_image(image, filename, hsv_filter, edge_detection=False):
  processed_image = process_image(image.copy(), hsv_filter, edge_detection)  # Process a copy
  cv2.imwrite(filename, processed_image)  # Save the processed image
  print(f"Image processed and saved as: {filename}")
def convert_to_maze_binary(image):
  if len(image.shape) == 3:
      gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  else:
      gray_img = image
  ret, binary_img = cv2.threshold(gray_img, 1, 255, cv2.THRESH_BINARY)
  inverted_img = cv2.bitwise_not(binary_img)
  return inverted_img
def read_bw_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Read image as grayscale

    # Apply a threshold to convert grayscale to binary (0 or 255)
    _, bw_image = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

    # Normalize to 0 or 1
    bw_array = 1 - bw_image // 255

    return bw_array
def write_array_to_file(array, filename):
  # Ensure data is a list or NumPy array
  if not isinstance(array, (list, np.ndarray)):
      raise TypeError("Input data must be a list or NumPy array.")
  # Open the file in write mode with truncation (deletes existing content)
  with open(filename, "w") as f:
    # Write each element of the array on a separate line
    for item in array:
      f.write(str(item) + "\n")  # Convert each item to string before writing
  print(f"Array successfully written to {filename}.")
def modify_array(array, center, height, width, value_to_replace_with):
    x_center, y_center = center
    half_height = height // 2
    half_width = width // 2

    
    y_start = max(0, y_center - half_height)
    y_end = min(len(array), y_center + half_height + 1)  
    x_start = max(0, x_center - half_width)
    x_end = min(len(array[0]), x_center + half_width + 1)  
    print(x_start,x_end,y_start,y_end)
  
    for y in range(y_start, y_end):
        for x in range(x_start, x_end):
            array[y][x] = int(value_to_replace_with)

    return array,x_start,x_end,y_start,y_end
def create_colored_image(array):
    color_map = {
        0: (0, 0, 0),   # Black
        1: (255, 0, 0), # Red
        2: (0, 0, 255), # Blue
        3: (0, 255, 0)  # Green
    }

    h, w = array.shape
    image_data = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            image_data[i, j] = color_map[array[i, j]]

    return Image.fromarray(image_data)
# Create a list of Marker objects
markers = []
for _, row in df.iterrows():
    markers.append(Marker(row['ID'], row['Center_X'], row['Center_Y'],
                          row['Height'], row['Width'], row['Angle_Degrees']))
# Example usage
Robot = next((m for m in markers if m.ID == 4), None)
Goal = next((m for m in markers if m.ID == 36), None)
#constants
MAX_PIXEL = max(Robot.height, Robot.width, Goal.height, Goal.width)
MAX_PIXEL= MAX_PIXEL/27.04156*30.6
if (MAX_PIXEL-int(MAX_PIXEL))>0:
    MAX_PIXEL = int(MAX_PIXEL)+1
else:
    MAX_PIXEL = int(MAX_PIXEL)
direction = 'NaN'
if Robot.angle>-100 and Robot.angle<-70:
    direction = 'D'
elif Robot.angle>70 and Robot.angle<100:
    direction = 'A'
elif Robot.angle>-10 or (Robot.angle<10 and Robot.angle>-170):
    direction = 'W'
elif Robot.angle>170 or Robot.angle<-170:
    direction = 'S'
else:
    direction = 'NaN'



hsv_filter_green = ((35, 50, 50), (75, 255, 255))  # Green
hsv_filter_red_dark = ((0, 100, 100), (10, 255, 255)) # Red (for darker shades)
hsv_filter_red_bright = ((170, 100, 100), (180, 255, 255)) # Red (for brighter shades)
hsv_filter_blue = ((100, 100, 100), (140, 255, 255))  # Blue
hsv_filter_brown = ((40, 0.2, 0.3), (50, 0.4, 1.0))

picname = "Map_Gen/RAW_MAP.png"
#picname = "Data/MAPPPPPP.png"
image = cv2.imread(picname) # read the image capture
height, width = image.shape[:2] # maze dimensions

save_processed_image(image.copy(), "Map_Gen/BIN_MAP.png", hsv_filter_red_dark)
cv2.imwrite("Map_Gen/FIN_MAP.png",convert_to_maze_binary(cv2.imread("Map_Gen/BIN_MAP.png")))

image_path = 'Map_Gen/FIN_MAP.png' 
bw_array = read_bw_image(image_path)
Robot.x = int(Robot.x)
Robot.y = int(Robot.y)
Goal.x = int(Goal.x)
Goal.y = int(Goal.y)

bw_array,x_start,x_end,y_start,y_end= modify_array(bw_array,(Robot.x,Robot.y),int(MAX_PIXEL+1),int(MAX_PIXEL+1),0)
bw_array,x_start,x_end,y_start,y_end= modify_array(bw_array,(Goal.x,Goal.y),int(MAX_PIXEL+1),int(MAX_PIXEL+1),0)
output_file = 'Map_Gen/map_clean.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(bw_array)
colored_image = create_colored_image(bw_array)
colored_image.save('Map_Gen/MAP_CLEAN.png')
print(f"Array written to {output_file}")

bw_array,rsx,rex,rsy,rey = modify_array(bw_array,(Robot.x,Robot.y),MAX_PIXEL,MAX_PIXEL,2)
bw_array,gsx,gex,gsy,gey = modify_array(bw_array,(Goal.x,Goal.y),MAX_PIXEL,MAX_PIXEL,3)
colored_image = create_colored_image(bw_array)
colored_image.save('Map_Gen/MAP_REP.png')
output_file = 'Map_Gen/map.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(bw_array)
print(f"Array written to {output_file}")


IRL = MAX_PIXEL/30.6
robotloc = [(rsx,rsy),(rex,rsy),(rex,rey),(rsx,rey)]
goalloc = [(gsx,gsy),(gex,gsy),(gex,gey),(gsx,gey)]
write_array_to_file([Robot.x,Robot.y,direction,IRL],'Map_Gen/map.txt')
write_array_to_file(robotloc,'Map_Gen/robot.txt')
write_array_to_file(goalloc,'Map_Gen/goal.txt')
print(MAX_PIXEL,direction)



