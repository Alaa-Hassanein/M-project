import cv2
import numpy as np

def auto_crop(img):
    # Load the image
    image = img#cv2.imread(image_path)

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define range for pink color in HSV
    lower_pink = np.array([140,50,50])
    upper_pink = np.array([160,255,255])

    # Threshold the HSV image to get only pink colors
    mask = cv2.inRange(hsv, lower_pink, upper_pink)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours based on area
    min_contour_area = 5000  # Set this to a suitable value
    contours = [c for c in contours if cv2.contourArea(c) > min_contour_area]

    # Find the rotated rectangles for all contours
    rects = [cv2.minAreaRect(c) for c in contours]

    # Calculate the area of each rectangle
    areas = [cv2.contourArea(cv2.boxPoints(rect)) for rect in rects]

    # Find the rectangle with the largest area
    rect = rects[np.argmax(areas)]

    # The rest of the code remains the same
    # Calculate the angle of rotation
    angle = rect[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Rotate the image to straighten the box
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # Crop the image to the box
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)

    cropped = rotated[y1:y2, x1:x2]

    return cropped

image = cv2.imread("C:/Users/alaah/Desktop/Screenshot 2024-06-04 124521.png")
image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
crop = auto_crop(image)
cv2.imshow("Show",crop)
cv2.waitKey(0)
