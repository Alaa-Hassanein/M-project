import cv2
import matplotlib.pyplot as plt
import numpy as np

img= cv2.imread('dasd')
fig,axs=plt.subplots(1,2,figsize=(30,30))
axs[0].imshow(img)
gray= cv2.cvtColor(img,cv2,COLOR_BGR2GRAY)
gray=np.float32(gray)

dst= cv2.cornerHarris(gray,2,3,0.04)

k =np,ones((7,7,np.uint8))
dst= cv2.dilate(dst,k)

img[dst_1>0.001*dst.max()]=[0,0,225]