import cv2, os
import numpy as np
from tqdm import tqdm
import uuid

from src.utils.videoio import save_video_with_watermark 

def paste_pic(video_path, pic_path, crop_info, new_audio_path, full_video_path, extended_crop=False):

    print("video_path", video_path)
    
    print("pic_path", pic_path)
   # pic_path = "./results/art_0_360.png"
    print("pic_path", pic_path)
    if not os.path.isfile(pic_path):
        print('ko thay file')



    if not os.path.isfile(pic_path):
        raise ValueError('pic_path must be a valid path to video/image file')
    elif pic_path.split('.')[-1] in ['jpg', 'png', 'jpeg']:
        # loader for first frame
        full_img = cv2.imread(pic_path)
        print("full_img", full_img)
    else:
        # loader for videos
        video_stream = cv2.VideoCapture(pic_path)
        fps = video_stream.get(cv2.CAP_PROP_FPS)
        full_frames = [] 
        while 1:
            still_reading, frame = video_stream.read()
            if not still_reading:
                video_stream.release()
                break 
            break 
        full_img = frame
    full_img = cv2.resize(full_img, (512,512))
    frame_h = full_img.shape[0]
    frame_w = full_img.shape[1]
    print("full_img", full_img.shape)




    value = 70  # Giá trị này có thể thay đổi tùy ý, tùy vào mức độ giảm sáng bạn muốn
    full_img = cv2.subtract(full_img, np.ones(full_img.shape, dtype="uint8") * value)


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

        test_img = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
        test_img = cv2.adaptiveThreshold(test_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 1)
        
        p = (crop_frame.astype(np.uint8))


        mask = 255*np.ones(p.shape, p.dtype)
        location = ((p.shape[0]) // 2, (p.shape[1]) // 2)
        gen_img = cv2.seamlessClone(p, full_img, mask, location, cv2.NORMAL_CLONE)
        for i in range (frame_h):
            for j in range(frame_w - 1):  # Change here to avoid index out of bound
                if test_img[i, j] == 0 and test_img[i, j + 1] == 255:  # Change here to correct the indices
                    gen_img[i, 0:j, :] = np.copy(full_img[i,0:j, :])
                    break
            for j in range(frame_w-1, 0, -1):
                if test_img[i, j] == 0 and test_img[i, j - 1] == 255:  # Change here to correct the indices
                    gen_img[i, j:frame_w-1, :] = np.copy(full_img[i, j:frame_w-1, :])
                    break
                
        
        out_tmp.write(gen_img)

    out_tmp.release()

    save_video_with_watermark(tmp_path, new_audio_path, full_video_path, watermark=False)

    video_stream = cv2.VideoCapture(full_video_path)
    fps = video_stream.get(cv2.CAP_PROP_FPS)
    crop_frames = []

    while True:
        still_reading, frame = video_stream.read()
        if not still_reading:
            video_stream.release()
            break
        crop_frames.append(frame)

# In frame đầu tiên để debug (chú ý: đoạn này có thể tạo ra output lớn tùy thuộc vào kích thước của frame)
    print("Frame đầu tiên:", crop_frames[0])


    
