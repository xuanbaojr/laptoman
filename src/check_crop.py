import cv2,torch, os
import numpy as np

from facexlib.detection import init_detection_model

class CheckCrop():
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        try:
            import webui  # in webui
            root_path = 'extensions/SadTalker/gfpgan/weights' 

        except:
            root_path = 'gfpgan/weights'

        self.det_net = init_detection_model('retinaface_resnet50', half=False,device=self.device, model_rootpath=root_path)

    def crop_or_not(self,input_path):
      #  input_path = './test/art_0.png'
        source_image= cv2.imread(input_path)
        h,w,c = source_image.shape
        w_face = self.eye_to_eye(source_image)
        ratio = (w_face/w)
        if ratio < 1:
            crop_or_full = 'crop'
        else:
            crop_or_full = 'full'
        return crop_or_full 
    
    def eye_to_eye(self, source_image):
        with torch.no_grad():
            img = np.array(source_image)
            bboxes = self.det_net.detect_faces(source_image, 0.97)
            w_face = bboxes[0][2] - bboxes[0][0]
        return w_face
    
if __name__ == "__main__":
    demo = CheckCrop()
    result = demo.crop_or_not(input_path='test/art_0.png')
    print(result)