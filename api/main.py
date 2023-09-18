import os, cv2
from src.inference import SadTalker
def sadtalker_demo(source_image, driven_audio, preprocess, still_mode, checkpoint_path='checkpoints', config_path='src/config', warpfn=None):
    
   
    sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)

    if os.path.exists(source_image):
        print("Source_image is exits!")
    else:
        print("Source_image is not exits!")

    result = sad_talker.test(source_image, driven_audio, preprocess, still_mode, use_enhancer = False)
    return result
    

if __name__ == "__main__":

    source_image = 'test/art_0.jpg'
    driven_audio = 'test/bus_chinese_out.wav'
    preprocess = "full"
    still_mode = False
    demo = sadtalker_demo(source_image, driven_audio, preprocess, still_mode )
    print(demo)

