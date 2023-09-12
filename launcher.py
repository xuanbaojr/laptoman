import cv2
import numpy as np

# Read grayscale image
image = cv2.imread('test/test5.png')
image_ = cv2.imread('test/test5.png')

# Changing black pixels to [110,255,0]
image[np.all(image == [0,0,0], axis=2)] = [255,255,255]
cv2.imwrite('test/result_img01.png', image)

image_test = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding

adaptive_threshold_image = cv2.adaptiveThreshold(image_test, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 50)

# This will set pixels to [110, 255, 0] where adaptive_threshold_image is 0, 
# otherwise it will keep the original values from `image`
image = np.where(adaptive_threshold_image[:, :, None] == 0, [255, 255, 255], image)
image = np.where(adaptive_threshold_image[:, :, None] == 0, [112,110,254], image)

adaptive_threshold_image = adaptive_threshold_image.astype(np.uint8)

kernel = np.ones((5,5), np.uint8)
adaptive_threshold_image = cv2.dilate(adaptive_threshold_image, kernel, iterations=1)


cv2.imwrite('test/result_img.png', image)
cv2.imwrite('test/threshold.png',adaptive_threshold_image)
