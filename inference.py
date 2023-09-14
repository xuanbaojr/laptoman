import cv2
import numpy as np
from rembg import remove

source_image = 'test/art_9.png'
output_path = 'test/test4.png'

with open(source_image, 'rb') as i:
    with open(output_path, 'wb') as o:
        input = i.read()
        output = remove(input)
        o.write(output)

test3 = cv2.imread(source_image)
test3 = cv2.resize(test3, (256,256))
test3_ = np.ones_like(test3)*100
h = test3.shape[0]
w = test3.shape[1]

test4 = cv2.imread(output_path)
test4 = cv2.resize(test4, (256,256))
test4_temp = cv2.imread(output_path)
test4_temp = cv2.resize(test4, (256,256))

blur_img = cv2.cvtColor(test4, cv2.COLOR_BGR2GRAY)
adaptive_threshold_image = cv2.adaptiveThreshold(blur_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 0.1)
#test3_ = np.where(adaptive_threshold_image[:,:,None] == 0, [255,255,255], test3)
#test4[np.where(adaptive_threshold_image == 0)] = [110,255,255]



kernel = np.ones((2,1), np.uint8)
adaptive_threshold_image = cv2.dilate(adaptive_threshold_image, kernel, iterations = 10)
# for i in range(5):

#     adaptive_threshold_image[h-1-i, 0:w-1] = 255
cv2.imwrite('test/threshold_img.png', adaptive_threshold_image)


# ...
contour_img = adaptive_threshold_image.copy()
contours, _ = cv2.findContours(contour_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest_contour = max(contours, key=cv2.contourArea)

# Tạo bản sao 3 kênh của adaptive_threshold_image
mask = np.zeros((h+2, w+2), dtype=np.uint8)
cv2.drawContours(test4, [largest_contour], 0, (255, 0, 0), thickness=1)
cv2.imwrite('test/test4_draw.png', test4)

#.....
array_y = []
for x in range(w):
    for y in range(h):
        if np.array_equal(test4[y, x], [255, 0, 0]):
            array_y.append((y, x))
            break

array_x = []
for y in range(h):
    for x in range(w):
        if np.array_equal(test4[y, x], [255, 0, 0]):
            array_x.append((y, x))
            break
    for x in range(w - 1, -1, -1):
        if np.array_equal(test4[y, x], [255, 0, 0]):
            array_x.append((y, x))
            break

# Gộp hai danh sách
unique_points = set(array_x + array_y)

for y, x in unique_points:
    test4[y, x] = [0, 0, 255]

cv2.imwrite('test/test4_draw_array.png', test4)





loDiff = (1, 20, 20)
upDiff = (255, 255, 254)
cv2.floodFill(test4, mask, (0, 0), (255, 255, 255), loDiff, upDiff)
cv2.floodFill(test4, mask, (w-1, 0), (255, 255, 255), loDiff, upDiff)
cv2.imwrite('test/test4_fill.png', test4)

test4_temp[np.where(np.all(test4 == [255, 0, 0], axis = 2))] = np.copy(test4_temp[np.where(np.all(test4 == [255, 0, 0], axis = 2))])
test4_temp[np.where(np.all(test4 == [255, 255, 255], axis = 2))] = np.copy(test3_[np.where(np.all(test4 == [255, 255, 255], axis = 2))])
test4_temp[np.where(np.all(test4 == [0, 0, 255], axis = 2))] = np.copy(test3_[np.where(np.all(test4 == [0, 0, 255], axis = 2))])

# test4 = np.where(test4[:,:,:] == [255,255,255], test3, test4)


#   test4 = np.where(test4[:,:,:] == [255,0,0], test3, test4)

cv2.imwrite('test/contour.png', test3)
cv2.imwrite('test/test4_.png', test4_temp)


