import cv2
import numpy as np

w=40
h=20
# Make empty black image
image=np.zeros((h,w,3),np.uint8)

# Fill left half with yellow
image[:,0:int(w/2)]=(0,255,255)

# Fill right half with blue
image[:,int(w/2):w]=(255,0,0)

# Create a named colour
red = [0,0,255]

# Change one pixel
image[10,5]=red

# Save
cv2.imwrite("result.png",image)
cv2.imshow("result.png",image)
cv2.waitKey(0)