import cv2, os
import numpy as np
from tqdm import tqdm
import uuid
from rembg import remove

from src.utils.videoio import save_video_with_watermark 

def paste_pic(video_path, pic_path, crop_info, new_audio_path, full_video_path, extended_crop=False):


    full_img = cv2.imread(pic_path)
    full_img = np.subtract((np.zeros_like(full_img)), 40 )
    
    
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
    frame_w = full_img.shape[0]
    frame_h = full_img.shape[1]
    full_img = full_img.astype(np.uint8)
    cv2.imwrite('./test/full_img.png', full_img)



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
    
    if len(crop_info) != 3:
        print("you didn't crop the image")
        return
    else:
        r_w, r_h = crop_info[0]
        clx, cly, crx, cry = crop_info[1]
        lx, ly, rx, ry = crop_info[2]
        lx, ly, rx, ry = int(lx), int(ly), int(rx), int(ry)
        # oy1, oy2, ox1, ox2 = cly+ly, cly+ry, clx+lx, clx+rx
        # oy1, oy2, ox1, ox2 = cly+ly, cly+ry, clx+lx, clx+rx

        if extended_crop:
            oy1, oy2, ox1, ox2 = cly, cry, clx, crx
        else:
            oy1, oy2, ox1, ox2 = cly+ly, cly+ry, clx+lx, clx+rx

    tmp_path = str(uuid.uuid4())+'.mp4'
    out_tmp = cv2.VideoWriter(tmp_path, cv2.VideoWriter_fourcc(*'MP4V'), fps, (frame_w, frame_h))
    for crop_frame in tqdm(crop_frames, 'seamlessClone:'):

        # p = (crop_frame.astype(np.uint8))
        # mask = 255*np.ones(p.shape, p.dtype)
        # location = ((p.shape[0]) // 2, (p.shape[1]) // 2)
        # gen_img = cv2.seamlessClone(p, full_img, mask, location, cv2.NORMAL_CLONE)
        crop_frame[np.all(crop_frame == (0,0,0), axis=2)] = [255,255,255]
        img_blur = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
        blur_img = cv2.blur(full_img, (49,49))
        adaptive_img = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 10)

        # adaptive_img = adaptive_img.astype(np.uint8)
        kernel = np.ones((30,30), np.uint8)
       # adaptive_img = cv2.dilate(adaptive_img, kernel, iterations=1)  

        array_1, array_2 = (np.where(adaptive_img == 0))
        array = np.column_stack((array_1, array_2))
        
        # for x,y in array:
        #     if y < frame_w//2:
        #         crop_frame[x,y:y+15] = np.copy(full_img[x,y:y+15])
        #     else:
        #         crop_frame[x,y:y-15] = np.copy(full_img[x,y:y-15])
      #  crop_frame = np.where(adaptive_img[:,:,None] == 0, [255,255,255], crop_frame)
        crop_frame = np.where(crop_frame[:,:,:] == [255,255,255], full_img, crop_frame)

        crop_frame = np.where(adaptive_img[:,:,None] == 0, full_img, crop_frame)
        crop_frame = crop_frame.astype(np.uint8)
      #  crop_frame = cv2.GaussianBlur(crop_frame, (15,15), 0)
        cv2.imwrite('haha.png',adaptive_img)
        out_tmp.write(crop_frame)
        

    out_tmp.release()

    save_video_with_watermark(tmp_path, new_audio_path, full_video_path, watermark=False)

#     video_stream = cv2.VideoCapture(full_video_path)
#     fps = video_stream.get(cv2.CAP_PROP_FPS)
#     crop_frames = []

#     while True:
#         still_reading, frame = video_stream.read()
#         if not still_reading:
#             video_stream.release()
#             break
#         crop_frames.append(frame)

# # In frame đầu tiên để debug (chú ý: đoạn này có thể tạo ra output lớn tùy thuộc vào kích thước của frame)
#     print("Frame đầu tiên:", crop_frames[0])
        # crop_frame = np.where(adaptive_img[:,:,None] == 0, [255,255,255], crop_frame)
        # crop_frame = np.where(crop_frame[:,:,:] == [255,255,255], full_img, crop_frame)
        # crop_frame = np.where(adaptive_img[:,:,None] == 0, full_img, crop_frame)