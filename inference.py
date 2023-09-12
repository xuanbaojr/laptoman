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
h = test3.shape[0]
w = test3.shape[1]

test4 = cv2.imread(output_path)
test4_ = cv2.imread(output_path)
test3_ = cv2.imread(source_image)

test3_blur = cv2.blur(test3, (51,51))
test4[np.all(test4 == [0,0,0], axis=2)] = [255,255,255]
blur_img = cv2.cvtColor(test4, cv2.COLOR_BGR2GRAY)
adaptive_threshold_image = cv2.adaptiveThreshold(blur_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 45, 65)
#test3_ = np.where(adaptive_threshold_image[:,:,None] == 0, [255,255,255], test3)

#test4[np.where(adaptive_threshold_image == 0)] = [110,255,255]

array_1, array_2 = (np.where(adaptive_threshold_image == 0))
array = np.column_stack((array_1, array_2))
print(array)

for x,y in array:
    if adaptive_threshold_image[x,y] == 0:
        if y < w//2 and y > 15:
            test3[x,y:y+15] = np.copy(test3[x,y-15:y])
cv2.imwrite('test/test3_.png', test3)
cv2.imwrite('test/test4_.png', test4_)
cv2.imwrite('test/threshold_img.png', adaptive_threshold_image)

