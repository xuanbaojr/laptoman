from src.utils.croper import Preprocesser

import cv2, torch, os
import numpy as np
from PIL import Image

class Image_Preprocess():
    def __init__(self):
        self.divice = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.preprocess = Preprocesser()

    def img_pre(self, input_path, xsize = 512):

        rate = 5
        rate_ = 2

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
        cry = int(cry + (rsize[1]-cry)/rate_)

        img_np = img_np[cly:cry, clx:crx]
        new_source_image = os.path.join('/results', pic_name + 'temp.png')
        cv2.imwrite(new_source_image, cv2.cvtColor(np.array(img_np), cv2.COLOR_RGB2BGR))
        return img_np