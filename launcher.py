import cv2, os
import numpy as np
from tqdm import tqdm
import uuid
from rembg import remove

from src.utils.videoio import save_video_with_watermark 

def paste_pic(video_path, pic_path, full_video_path, extended_crop=False):


    full_img = cv2.imread(pic_path)
    if not os.path.isfile(pic_path):
        print("ko co file")
   # full_img = np.subtract((np.zeros_like(full_img)), 40 )
    
    
    # w,h = full_img.shape[:2]

    # output_path = './test/test4.png'

    # with open(pic_path, 'rb') as i:
    #     with open(output_path, 'wb') as o:
    #         input = i.read()
    #         output = remove(input)
    #         o.write(output)
    # crop_img = cv2.imread(output_path)

    # crop_img[np.all(crop_img == [0,0,0], axis = 2)] = [255,255,255]
    # blur_crop = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # adaptive_crop = cv2.adaptiveThreshold(blur_crop, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 35, 45)



    # array_crop_1, array_crop_2 = (np.where(adaptive_crop == 0))
    # array_crop = np.column_stack((array_crop_1, array_crop_2))
    # for x,y in array_crop:
    #     if y < w//2:
    #         full_img[x,y:y+y] = np.copy(np.fliplr(full_img[x, 0 : y]))
    #     if y > w//2  and y < w :
    #         y_r = w - y
    #         full_img[x,y-y_r + 1:y] =  np.copy(np.fliplr(full_img[x, y:y + y_r -1]))
    full_img = cv2.resize(full_img, (256,256))
    w = full_img.shape[0]
    h = full_img.shape[1]
    full_img = full_img.astype(np.uint8)
    cv2.imwrite('./test/full_img.png', full_img)
    test3 = cv2.imread('./test/full_img.png')
    test3 = cv2.resize(test3, (256,256))
    test3_ = np.ones_like(test3)*120
    test3_blur = cv2.blur(test3, (51,51))



    video_stream = cv2.VideoCapture(video_path)
    fps = video_stream.get(cv2.CAP_PROP_FPS)
    crop_frames = []
    while 1:
        still_reading, frame = video_stream.read()
        if not still_reading:
            video_stream.release()
            break
        crop_frames.append(frame)
    
    print("crop_frame", crop_frames[0].shape)
    cv2.imwrite('./test/haha.png', crop_frames[0])

    tmp_path = './test/output.mp4'
    out_tmp = cv2.VideoWriter(tmp_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (w, h))

    for frame in tqdm(crop_frames, 'SeamlessClone:'):
     #   test4 = cv2.imread('test/haha.png')
        test4 = cv2.resize(frame, (256,256))
        test4 = cv2.resize(frame, (256,256))
   #     test4_temp = cv2.imread(output_path)
        test4_temp = cv2.resize(test4, (256,256))

        blur_img = cv2.cvtColor(test4, cv2.COLOR_BGR2GRAY)
        adaptive_threshold_image = cv2.adaptiveThreshold(blur_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 45, 2)
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

        target_color = [255, 0, 0]

        # Tìm tất cả các điểm có màu [255, 0, 0]
        indices = np.where(np.all(test4 == target_color, axis=-1))

        # Tạo danh sách tọa độ
        points = list(zip(indices[0], indices[1]))

        # comprehension
        array_y = []
        for x in range(w):
            col_indices = [point for point in points if point[1] == x]
            if col_indices:
                array_y.append(col_indices[0])

        array_x = []
        for y in range(h):
            row_indices = [point for point in points if point[0] == y]
            if row_indices:
                array_x.extend([row_indices[0], row_indices[-1]])

        unique_points = set(array_x + array_y)


        for y, x in unique_points:
            test4[y, x] = [0, 0, 255]

        cv2.imwrite('test/test4_draw_array.png', test4)





        loDiff = (10, 20, 20)
        upDiff = (255, 255, 254)
        cv2.floodFill(test4, mask, (0, 0), (255, 255, 255), loDiff, upDiff)
        cv2.imwrite('test/test4_fill.png', test4)

        test4_temp[np.where(np.all(test4 == [255, 0, 0], axis = 2))] = np.copy(test4_temp[np.where(np.all(test4 == [255, 0, 0], axis = 2))])
        test4_temp[np.where(np.all(test4 == [255, 255, 255], axis = 2))] = np.copy(test3[np.where(np.all(test4 == [255, 255, 255], axis = 2))])
        test4_temp[np.where(np.all(test4 == [0, 0, 255], axis = 2))] = np.copy(test3[np.where(np.all(test4 == [0, 0, 255], axis = 2))])

        # test4 = np.where(test4[:,:,:] == [255,255,255], test3, test4)


        #   test4 = np.where(test4[:,:,:] == [255,0,0], test3, test4)

        cv2.imwrite('test/contour.png', test3)
        cv2.imwrite('test/test4_.png', test4_temp)




        
        out_tmp.write(test4_temp)
    out_tmp.release()

#     for crop_frame in tqdm(crop_frames, 'seamlessClone:'):

        
        
#         # p = (crop_frame.astype(np.uint8))
#         # mask = 255*np.ones(p.shape, p.dtype)
#         # location = ((p.shape[0]) // 2, (p.shape[1]) // 2)
#         # gen_img = cv2.seamlessClone(p, full_img, mask, location, cv2.NORMAL_CLONE)
#       #  crop_frame[np.all(crop_frame == (0,0,0), axis=2)] = [255,255,255]
#         img_blur = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
#         blur_img = cv2.blur(full_img, (49,49))
#         adaptive_img = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 1)

#         # adaptive_img = adaptive_img.astype(np.uint8)
#         kernel = np.ones((2,1), np.uint8)
#        # adaptive_img = cv2.dilate(adaptive_img, kernel, iterations=1)  

#         array_1, array_2 = (np.where(adaptive_img == 0))
#         array = np.column_stack((array_1, array_2))

#         adaptive_img = cv2.dilate(adaptive_img, kernel, iterations=10)

#         contour_img = adaptive_img.copy()
#         contours, _ = cv2.findContours(contour_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         largest_contour = max(contours, key=cv2.contourArea)

#         mask = np.zeros((frame_h+2, frame_w+2), dtype=np.uint8)
#         cv2.drawContours(crop_frame, [largest_contour], 0, (255, 0, 0), 3)
#         loDiff = (50, 50, 255)
#         upDiff = (50, 50, 255)
#         cv2.floodFill(crop_frame, mask, (0, 0), (255, 255, 255), loDiff, upDiff)

# # test4[np.where(np.all(contour_img_color == [100, 255, 0], axis = 2))] = [0,0,0]
#         crop_frame = np.where(crop_frame[:,:,:] == [255,255,255], full_img, crop_frame)
#         crop_frame = np.where(crop_frame[:,:,:] == [255,0,0], full_img, crop_frame)


#         crop_frame = crop_frame.astype(np.uint8)
#       #  crop_frame = cv2.GaussianBlur(crop_frame, (15,15), 0)
#         cv2.imwrite('./test/hah01.png', crop_frame)
#         out_tmp.write(crop_frame)
        

#     out_tmp.release()

  #  save_video_with_watermark(tmp_path, new_audio_path = './test/bus_chinese.wav', full_video_path = full_video_path, watermark=False)

if __name__ == "__main__":

    video_path = './test/video.mp4'
    pic_path = './test/art_0.png'
    full_video_path = './test/output.mp4'
    demo = paste_pic(video_path, pic_path, full_video_path = full_video_path)
    print(demo)