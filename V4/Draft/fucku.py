import cv2
import numpy as np

# Load your pre-corrected image (replace 'your_image.jpg' with the actual file path)
image = cv2.imread('bool.png', cv2.IMREAD_GRAYSCALE)

# Apply edge detection (Canny)
edges = cv2.Canny(image, 30, 250, apertureSize=3)
minLineLength = 200
maxLineGap = 10
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0),thickness=1)
ret, thresh = cv2.threshold(image,0,255,0)
likew, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for hi in likew:
    cv2.drawContours(image, [hi], -1, (255, 255, 255),-1)
# Save the output image (replace 'output_image.jpg' with your desired output file path)
cv2.imwrite('output_image.jpg', image)
print("Pixelated lines straightened and saved as 'output_image.jpg'")
