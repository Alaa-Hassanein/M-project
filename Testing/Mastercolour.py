import cv2
import numpy as np

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

import cv2

import cv2

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

save_processed_image(image.copy(), "goal.jpg", hsv_filter_green)
save_processed_image(image.copy(), "robot.jpg", hsv_filter_blue)
save_processed_image(image.copy(), "map.jpg", hsv_filter_red_dark)