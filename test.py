import cv2 
import numpy as np

# Load image
im = cv2.imread('maze.jpg')

# Define the blue colour we want to find - remember OpenCV uses BGR ordering
blue = [0,0,0]
green = [0,0,0]

# Get X and Y coordinates of all blue pixels
Yb, Xb = np.where(np.all(im==blue,axis=2))

for i in range(0,len(Xb)):
    upper=(Xb[i],Yb[i])

 
print (upper)
