import cv2
import numpy as np

# Read grayscale image
image = cv2.imread('test/test.png')
for i in range(322):
    for j in range(248):
        if (image[i,j] == np.array([0,0,0])).all():
            image[i,j] = [255,255,0]
#cv2.imshow('Original1', image)
cv2.imwrite('test/result_img01.png', image)


if image is None:
    print("Could not read the image.")
    exit()

h, w = image.shape[:2]
image_test = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image_bg = cv2.imread('test/art_0_360.png')

if image_bg is None:
    print("Could not read the background image.")
    exit()

image_bg = cv2.resize(image_bg, (w, h))

# Apply adaptive thresholding
adaptive_threshold_image = cv2.adaptiveThreshold(image_test, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 20, 10)

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

cv2.imshow('Original', image)
cv2.imshow('Adaptive Threshold', adaptive_threshold_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
