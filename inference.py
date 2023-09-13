import cv2
import numpy as np
from rembg import remove

source_image = 'test/test3.png'
output_path = 'test/test4.png'

with open(source_image, 'rb') as i:
    with open(output_path, 'wb') as o:
        input = i.read()
        output = remove(input)
        o.write(output)

test3 = cv2.imread(source_image)
test3_ = np.ones_like(test3)*100
h = test3.shape[0]
w = test3.shape[1]

test4 = cv2.imread(output_path)
blur_img = cv2.cvtColor(test4, cv2.COLOR_BGR2GRAY)
adaptive_threshold_image = cv2.adaptiveThreshold(blur_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 1)
#test3_ = np.where(adaptive_threshold_image[:,:,None] == 0, [255,255,255], test3)
#test4[np.where(adaptive_threshold_image == 0)] = [110,255,255]



kernel = np.ones((2,1), np.uint8)
adaptive_threshold_image = cv2.dilate(adaptive_threshold_image, kernel, iterations = 10)
cv2.imwrite('test/threshold_img.png', adaptive_threshold_image)


# ...
contour_img = adaptive_threshold_image.copy()
contours, _ = cv2.findContours(contour_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest_contour = max(contours, key=cv2.contourArea)

# Tạo bản sao 3 kênh của adaptive_threshold_image
mask = np.zeros((h+2, w+2), dtype=np.uint8)
cv2.drawContours(test4, [largest_contour], 0, (255, 0, 0), 3)
loDiff = (50, 50, 255)
upDiff = (50, 50, 255)
cv2.floodFill(test4, mask, (0, 0), (255, 255, 255), loDiff, upDiff)

# test4[np.where(np.all(contour_img_color == [100, 255, 0], axis = 2))] = [0,0,0]
test4 = np.where(test4[:,:,:] == [255,255,255], test3_, test4)
test4 = np.where(test4[:,:,:] == [255,0,0], test3_, test4)


# ...


cv2.imwrite('test/contour.png', test3)
cv2.imwrite('test/test4_.png', test4)


