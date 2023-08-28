import cv2, os
import numpy as np
from tqdm import tqdm
import uuid

from src.utils.videoio import save_video_with_watermark 

def paste_vid(head_video, body_video, crop_info, new_audio_path, full_video_path, body_h, body_w):

    print("head_video", head_video)
    print("body_video", body_video)
    if not os.path.isfile(head_video):
        print('ko thay file')

    video_head = cv2.VideoCapture(head_video)
    fps = 25
    full_frame_head = []
    while 1:
        still_reading, frame = video_head.read()
        if not still_reading:
            video_head.release()
            break
        full_frame_head.append(frame)
     
    video_body = cv2.VideoCapture(body_video)
    fps = 25
    full_frame_body = []
    while 1:
        still_reading, frame = video_body.read()
        if not still_reading:
            video_body.release()
            break
        full_frame_body.append(frame)
    
   # crop_info = (45, 13, 363, 332)
    clx, cly, crx, cry = crop_info[1]

    frame_w = 256
    frame_h = 256

    head_w = int(256*((crx - clx)/ body_w))
    head_h = int(256*((cry - cly)/ body_h))

    location_w = int(256*((clx+crx)//2)/ body_w)
    location_h = int(256*((cly+cry)//2)/ body_h)

    tmp_path = str(uuid.uuid4())+'.mp4'
    out_tmp = cv2.VideoWriter(tmp_path, cv2.VideoWriter_fourcc(*'MP4V'), fps, (frame_w, frame_h))
    for key in tqdm(range(len(full_frame_head)), 'Dang noi video'):
        head = cv2.resize(full_frame_head[key].astype(np.uint8), (head_w, head_h))
        mask = 255*np.ones(head.shape, head.dtype)
        location = (location_h, location_w )
        gen_img = cv2.seamlessClone(head, full_frame_body[key], mask, location, cv2.NORMAL_CLONE)
        out_tmp.write(gen_img)

    out_tmp.release()
    print("dang noi video")
    save_video_with_watermark(tmp_path, new_audio_path, full_video_path, watermark=False)
    os.remove(tmp_path)
    


