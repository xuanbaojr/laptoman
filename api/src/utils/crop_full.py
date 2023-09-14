import os
import uuid

import cv2
import numpy as np
from tqdm import tqdm

from src.utils.videoio import save_video_with_watermark


def crop_full(full_video_path, crop_info, new_audio_path, av_path):

    rate = 8
    rate_ = 5

    pic_name = os.path.splitext(os.path.split(input_path)[-1])[0]


    if not os.path.isfile(input_path):
        raise ValueError('input_path must be a valid path to video/image file')
    elif input_path.split('.')[-1] in ['jpg', 'png', 'jpeg']:
        # loader for first frame
        full_frames = [cv2.imread(input_path)]
        fps = 25
    else:
        # loader for videos
        video_stream = cv2.VideoCapture(input_path)
        fps = video_stream.get(cv2.CAP_PROP_FPS)
        full_frames = [] 
        while 1:
            still_reading, frame = video_stream.read()
            if not still_reading:
                video_stream.release()
                break 
            full_frames.append(frame) 


    x_full_frames= [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  for frame in full_frames] 
    img_np = x_full_frames[0]
    lm = self.preprocess.get_landmark(img_np)

    rsize, crop, _ = self.preprocess.align_face(img = Image.fromarray(img_np), lm = lm, output_size=xsize)
    clx, cly, crx, cry = crop
    img_np = cv2.resize(img_np, (rsize[0], rsize[1]))

    crx = int(crx + min(clx,rsize[0]-crx)/rate)
    clx = int(clx - min(clx,rsize[0]-crx)/rate)
    cly = int(cly - min(cly,rsize[1]-cry)/rate_)
    cry = min(int(cry + (cry - cly)/rate_), rsize[1])

    img_np = img_np[cly:cry, clx:crx]
    new_source_image = os.path.join('results', pic_name + '.png')
    cv2.imwrite(new_source_image, cv2.cvtColor(np.array(img_np), cv2.COLOR_RGB2BGR))
    print("new", new_source_image)
    return new_source_image
    print("hahahahaha")