import cv2
import numpy as np

# Read grayscale image
image = cv2.imread('test/test.png')
h, w = image.shape[:2]

for i in range(h):
    for j in range(w):
        if (image[i,j] == np.array([0,0,0])).all():
            image[i,j] = [255,255,0]
#cv2.imshow('Original1', image)
cv2.imwrite('test/result_img01.png', image)



image_test = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding
adaptive_threshold_image = cv2.adaptiveThreshold(image_test, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

# Loop to manipulate image
for i in range(h):
    for j in range(w - 1):  # Change here to avoid index out of bound
        if adaptive_threshold_image[i, j] == 0 and adaptive_threshold_image[i, j + 1] == 255:  # Change here to correct the indices
            image[i, 0:j, :] = [0,0,0]
            break
    for j in range(w-1, 0, -1):
        if adaptive_threshold_image[i, j] == 0 and adaptive_threshold_image[i, j - 1] == 255:  # Change here to correct the indices
            image[i, j:w-1, :] = [0,0,0]
            break

# Show images
for i in range(h):
    for j in range(w):
        if (image[i,j] == np.array([0,0,0])).all():
            image[i,j] = [255,255,0]
cv2.imwrite('test/result_img.png', image)


