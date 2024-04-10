import cv2
import numpy as np
from PIL import Image
import os

def capture_and_save_image(filename="all.jpg"):
  # Capture video from the default camera (index 0)
  cap = cv2.VideoCapture(0)

  # Check if camera opened successfully
  if not cap.isOpened():
      print("Error opening camera!")
      return False

  # Capture a single frame
  ret, frame = cap.read()

  # Check if frame capture was successful
  if not ret:
      print("Failed to capture frame!")
      cap.release()
      return False

  # Save the frame
  cv2.imwrite(filename, frame)

  # Release the camera
  cap.release()

  print(f"Image captured and saved as {filename}")

def process_image(image, hsv_filter, edge_detection=False):
  """
  Processes an image in memory, applying color filtering based on HSV values and edge detection (optional).

  Args:
      image (numpy.ndarray): The image data as a NumPy array.
      hsv_filter (tuple): A tuple of HSV values (0-179, 0-255, 0-255) defining the filter range.
      edge_detection (bool, optional): Whether to perform edge detection. Defaults to False.

  Returns:
      numpy.ndarray: The processed image data.
  """

  # Convert image to BGR format if needed (assuming OpenCV default)
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
  """
  Processes an image, applies filters based on HSV values and edge detection (optional), and saves it.

  Args:
      image (numpy.ndarray): The image data as a NumPy array.
      filename (str): The filename to save the processed image as.
      hsv_filter (tuple): A tuple of HSV values (0-179, 0-255, 0-255) defining the filter range.
      edge_detection (bool, optional): Whether to perform edge detection. Defaults to False.
  """

  processed_image = process_image(image.copy(), hsv_filter, edge_detection)  # Process a copy
  cv2.imwrite(filename, processed_image)  # Save the processed image
  print(f"Image processed and saved as: {filename}")


def convert_to_maze_binary(image):
  """
  Converts an image to a binary image with white foreground and black background, then inverts it.

  Args:
      image (numpy.ndarray): The image data as a NumPy array.

  Returns:
      numpy.ndarray: The inverted binary image data with white foreground and black background.
  """

  # Convert image to grayscale if needed (assuming OpenCV default)
  if len(image.shape) == 3:
      gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  else:
      gray_img = image

  # Threshold to binary with white foreground (assuming black background)
  ret, binary_img = cv2.threshold(gray_img, 1, 255, cv2.THRESH_BINARY)  # Adjust threshold if needed

  # Invert the binary image (white becomes black, black becomes white)
  inverted_img = cv2.bitwise_not(binary_img)

  return inverted_img

def convert_to_binary(image):
  """
  Converts an image to a binary image with white foreground and black background, then inverts it.

  Args:
      image (numpy.ndarray): The image data as a NumPy array.

  Returns:
      numpy.ndarray: The inverted binary image data with white foreground and black background.
  """

  # Convert image to grayscale if needed (assuming OpenCV default)
  if len(image.shape) == 3:
      gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  else:
      gray_img = image

  # Threshold to binary with white foreground (assuming black background)
  ret, binary_img = cv2.threshold(gray_img, 1, 255, cv2.THRESH_BINARY)  # Adjust threshold if needed

  # Invert the binary image (white becomes black, black becomes white)

  return binary_img


def find_object(image):
  """
  Finds a single object in an image with a black background.

  Args:
      image (numpy.ndarray): The image data as a NumPy array (assuming black background and single object).

  Returns:
      tuple: A tuple containing (is_object_found, bounding_box, center, radius)
          - is_object_found (bool): True if a colored object is found, False otherwise.
          - bounding_box (tuple): A tuple representing the bounding box (x, y, width, height) of the object.
          - center (tuple): A tuple representing the center coordinates (x, y) of the object.
          - radius (float): The estimated radius of the object (approximated as a circle).
  """

  # Find contours
  contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Check if any contours are found
  if not contours:
      return False, None, None, None

  # Assuming the largest contour corresponds to the object (adjust if needed)
  largest_contour = max(contours, key=cv2.contourArea)

  # Find bounding box, center, and radius (approximated as a circle)
  x, y, w, h = cv2.boundingRect(largest_contour)
  center = (int(x + w / 2), int(y + h / 2))
  radius = max(w // 2, h // 2)  # Approximate radius based on bounding box dimensions

  return True, (x, y, w, h), center, radius

def write_array_to_file(array, filename="loc.txt"):
  """
  Writes an array to a text file, handling existing file deletion or clearing.

  Args:
      array (list): The list or NumPy array to write to the file.
      filename (str, optional): The filename to use. Defaults to "loc.txt".
  """

  # Ensure data is a list or NumPy array
  if not isinstance(array, (list, np.ndarray)):
      raise TypeError("Input data must be a list or NumPy array.")

  # Open the file in write mode with truncation (deletes existing content)
  with open(filename, "w") as f:
    # Write each element of the array on a separate line
    for item in array:
      f.write(str(item) + "\n")  # Convert each item to string before writing

  print(f"Array successfully written to {filename}.")


picname = "all.jpg"
#capture_and_save_image(picname) 
image = cv2.imread(picname)

# Green
hsv_filter_green = ((35, 50, 50), (75, 255, 255))  # Adjustable for specific green tones

# Red (for darker shades)
hsv_filter_red_dark = ((0, 100, 100), (10, 255, 255))  # Adjustable for variations

# Red (for brighter shades)
hsv_filter_red_bright = ((170, 100, 100), (180, 255, 255))  # Adjustable for variations

# Blue
hsv_filter_blue = ((100, 100, 100), (140, 255, 255))  # Adjustable for specific blue tones

save_processed_image(image.copy(), "goal.png", hsv_filter_green)
save_processed_image(image.copy(), "robot.png", hsv_filter_blue)
save_processed_image(image.copy(), "map.png", hsv_filter_red_dark)

binary_map = cv2.imwrite("binary.jpg",convert_to_maze_binary(cv2.imread("map.png")))
binary_robot = cv2.imwrite("robotb.jpg",convert_to_binary(cv2.imread("robot.png")))
binary_goal = cv2.imwrite("goalb.jpg",convert_to_binary(cv2.imread("goal.png")))

# Convert the image to a NumPy array
robotloc = np.array(Image.open("robotb.jpg"))
goalloc = np.array(Image.open("goalb.jpg"))
# Example usage (assuming you have loaded your image data into a variable named 'image')
roboty, rbounding_box, rcenter, rradius = find_object(robotloc)

goaly, gbounding_box, gcenter, gradius = find_object(goalloc)
if roboty:
  print("robot")
  print(f"Bounding box: {rbounding_box}")
  print(f"Center: {rcenter}")
  print(f"Radius: {rradius}")

if goaly:
  print("goal")
  print(f"Bounding box: {gbounding_box}")
  print(f"Center: {gcenter}")
  print(f"Radius: {gradius}")

lines = [
    rcenter,
    gcenter
]

write_array_to_file(lines)