from src.utils.croper import Preprocesser

import cv2, torch
import numpy as np
from PIL import Image

class Image_Preprocess():
    def __init__(self):
        self.divice = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.preprocess = Preprocesser()

    def img_pre(self, source_image, xsize = 512):

        rate = 5
        rate_ = 2

        img_np = np.array(source_image)
        lm = self.preprocess.get_landmark(img_np)

        rsize, crop, _ = self.preprocess.align_face(img = Image.fromarray(img_np), lm = lm, output_size=xsize)
        clx, cly, crx, cry = crop
        img_np = cv2.resize(img_np, (rsize[0], rsize[1]))

        crx = int(crx + min(clx,rsize[0]-crx)/rate)
        clx = int(clx - min(clx,rsize[0]-crx)/rate)
        cly = int(cly - min(cly,rsize[1]-cry)/rate_)
        cry = int(cry + (rsize[1]-cry)/rate_)

        img_np = img_np[cly:cry, clx:crx]

        return img_np