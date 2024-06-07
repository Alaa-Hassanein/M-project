import pandas as pd
import cv2
import numpy as np
from PIL import Image
import csv
import os
from rembg import remove



def crop_center(img, new_width, new_height):

    # Get the original dimensions
    height, width= img.shape

    # Calculate the cropping coordinates
    x = (width - new_width) // 2
    y = (height - new_height) // 2

    # Crop the center portion of the image
    cropped_img = img[y:y+new_height, x:x+new_width]

    # Save the cropped image (optional)
    #cv2.imwrite("cropped_image.jpg", cropped_img)

    return cropped_img

def overlay_images(img1, img2):

    # Get the dimensions of the images
    h1, w1= img1.shape
    h2, w2= img2.shape

    # Calculate the position to overlay img1 on img2 (centered)
    x_offset = (w2 - w1) // 2
    y_offset = (h2 - h1) // 2

    # Overlay img1 on img2
    img2[y_offset:y_offset+h1, x_offset:x_offset+w1] = img1

    # Save the result
    #cv2.imwrite(output_path, img2)
    return img2

def filler(img):
    cropped = crop_center(img, 1080, 1918)
    ret, thresh = cv2.threshold(cropped,0,255,0)
    likew, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for hi in likew:
        cv2.drawContours(cropped, [hi], -1, (255, 255, 255),-1)
    final =np.zeros_like(img)
    final = overlay_images(cropped,final)
    #print(final.shape)
    #cv2.imshow('Image with Corners', final)
    #cv2.imwrite("final.jpg",finals)
    #cv2.waitKey(0)
    return final



# Read the CSV file into a pandas DataFrame
df = pd.read_csv('V4/Map_Gen/aruco_markers.csv')
# Define the Marker class
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
def love2(image,rgb = (181, 25, 110)):
    img = image
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    def extract_color(image, target_rgb, tolerance=80):
        lower_bound = np.array([max(0, c - tolerance) for c in target_rgb], dtype=np.uint8)
        upper_bound = np.array([min(255, c + tolerance) for c in target_rgb], dtype=np.uint8)

        mask = cv2.inRange(image, lower_bound, upper_bound)
        extracted_color = cv2.bitwise_and(image, image, mask=mask)

        return extracted_color
    target_rgb = rgb
    #cv2.imwrite("1001.jpg",img_hsv)
    extracted_regions = extract_color(cv2.cvtColor(img_hsv,cv2.COLOR_BGR2RGB), target_rgb)
    cv2.imwrite("bool.png",extracted_regions)
        
    # Apply edge detection (Canny)
    extracted_regions = cv2.cvtColor(extracted_regions,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(extracted_regions, 30, 250, apertureSize=3)
    minLineLength = 200
    maxLineGap = 10
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0),thickness=1)
    ret, thresh = cv2.threshold(extracted_regions,0,255,0)
    #extracted_regions = filler(extracted_regions)
    #likew, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #for hi in likew:
    #    cv2.drawContours(extracted_regions, [hi], -1, (255, 255, 255),-1)
    # Save the output image (replace 'output_image.jpg' with your desired output file path)
    cv2.imwrite('output_image.jpg', extracted_regions)
    print("Pixelated lines straightened and saved as 'output_image.jpg'")
    return extracted_regions
def processhsv_image(image, hsv_filter, edge_detection):
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
def process_image(image, color_space, filter, edge_detection):
    if len(image.shape) == 2:  # Grayscale image
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    elif image.shape[2] != 3:  # Non-BGR color format
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

    if color_space.lower() == 'hsv':
        # Color filtering based on HSV values
        lower_hsv = np.array(filter[0])
        upper_hsv = np.array(filter[1])
        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # Convert to HSV color space
        mask = cv2.inRange(hsv_img, lower_hsv, upper_hsv)  # Create mask for the HSV range
        image = cv2.bitwise_and(image, image, mask=mask)  # Apply mask
    elif color_space.lower() == 'rgb':
        # Color filtering based on RGB values (you can define your own thresholds)
        lower_rgb = np.array(filter[0])
        upper_rgb = np.array(filter[1])
        mask = cv2.inRange(image, lower_rgb, upper_rgb)  # Create mask for the RGB range
        image = cv2.bitwise_and(image, image, mask=mask)  # Apply mask

    # Edge detection (using Sobel filter)
    if edge_detection:
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        sobelx = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=5)  # Sobel filter for horizontal edges
        sobely = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=5)  # Sobel filter for vertical edges
        edges = cv2.bitwise_or(sobelx, sobely)  # Combine horizontal and vertical edges
        image = edges  # Replace original image with edge detection result

    return image
def save_processed_image(image, filename): #, filter, edge_detection=False color_space,
  processed_image = love2(image) #process_image(image.copy(),color_space, filter, edge_detection)  # Process a copy
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
markers = []
picname = "V4/Map_Gen/QWERTY_MAP.png"
#picname = "C:/Users/Aditya/Downloads/Screenshot 2024-06-04 123654.png"
#picname = 'V4/Map_Gen/image.png'
image = cv2.imread(picname)
for _, row in df.iterrows():
    markers.append(Marker(row['ID'], row['Center_X'], row['Center_Y'],
                          row['Height'], row['Width'], row['Angle_Degrees'],
                          row['Top_Left_X'],row['Top_Left_Y'],
                          row['Top_Right_X'],row['Top_Right_Y'],
                          row['Bottom_Left_X'],row['Bottom_Left_Y'],
                          row['Bottom_Right_X'],row['Bottom_Right_Y']))
Robot = next((m for m in markers if m.ID == 4), None)
Goal = next((m for m in markers if m.ID == 36), None)
MAX_PIXEL= image.shape[1]/1.83*0.3
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
hsv_filter_teal = ((190, 20, 40), (220, 255, 255)) #tape 
rgb_filter_teal = ((113, 141, 165), (122, 140, 149)) #tape


#dst = cv2.imwrite("confrim.png",remove(image)) # read the image capture
#rows,cols,ch = image.shape
#pts1 = np.float32([[Track1.Top_Right_X,Track1.Top_Right_Y],[Track2.Top_Left_X,Track2.Top_Left_Y],[Track3.Bottom_Right_X,Track3.Bottom_Right_Y],[Track4.Bottom_Left_X,Track4.Bottom_Left_Y]])
#pts2 = np.float32([[0,0],[1080,0],[1080,1920],[0,1920]])
#M = cv2.getPerspectiveTransform(pts1,pts2)
#image = cv2.warpPerspective(image,M,(cols,rows))

#cv2.imwrite("trial.png",image)

height, width = image.shape[:2] # maze dimensions

save_processed_image(image.copy(),"V4/Map_Gen/BIN_MAP.png")
cv2.imwrite("V4/Map_Gen/FIN_MAP.png",convert_to_maze_binary(cv2.imread("V4/Map_Gen/BIN_MAP.png")))

image_path = 'V4/Map_Gen/FIN_MAP.png' 
bw_array = read_bw_image(image_path)
Robot.x = int(Robot.x)
Robot.y = int(Robot.y)
Goal.x = int(Goal.x)
Goal.y = int(Goal.y)

bw_array,x_start,x_end,y_start,y_end= modify_array(bw_array,(Robot.x,Robot.y),int(MAX_PIXEL+1),int(MAX_PIXEL+1),0)
bw_array,x_start,x_end,y_start,y_end= modify_array(bw_array,(Goal.x,Goal.y),int(MAX_PIXEL+1),int(MAX_PIXEL+1),0)
output_file = 'V4/Map_Gen/map_clean.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(bw_array)
colored_image = create_colored_image(bw_array)
colored_image.save('V4/Map_Gen/MAP_CLEAN.png')
print(f"Array written to {output_file}")

bw_array,rsx,rex,rsy,rey = modify_array(bw_array,(Robot.x,Robot.y),MAX_PIXEL,MAX_PIXEL,2)
bw_array,x_start,x_end,y_start,y_end= modify_array(bw_array,(Robot.x,Robot.y),int(MAX_PIXEL*1.5),int(MAX_PIXEL*1.5),0)
bw_array,gsx,gex,gsy,gey = modify_array(bw_array,(Goal.x,Goal.y),MAX_PIXEL+10,MAX_PIXEL+10,3)
#bw_array,rsx,rex,rsy,rey = modify_array(bw_array,(Robot.x,Robot.y),MAX_PIXEL,MAX_PIXEL,2)

colored_image = create_colored_image(bw_array)
colored_image.save('V4/Map_Gen/MAP_REP.png')
output_file = 'V4/Map_Gen/map.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(bw_array)
print(f"Array written to {output_file}")


IRL = 183/image.shape[1]
robotloc = [(rsx,rsy),(rex,rsy),(rex,rey),(rsx,rey)]
goalloc = [(gsx,gsy),(gex,gsy),(gex,gey),(gsx,gey)]
write_array_to_file([direction,IRL],'V4/Map_Gen/map.txt')
write_array_to_file(robotloc,'V4/Map_Gen/robot.txt')
write_array_to_file(goalloc,'V4/Map_Gen/goal.txt')
print(MAX_PIXEL,direction)



