import os
from src.gradio_demo import SadTalker
from src.check_crop import CheckCrop
# warpfn , lazy_load ?
def sadtalker_demo(checkpoint_path='checkpoints', config_path='src/config', warpfn=None):
    sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)
    # source image :
    source_image = 'test/test.jpg'
    driven_audio = 'test/bus_chinese.wav'

    if os.path.exists(source_image):
        print("Đường dẫn source_image đúng!")
    else:
        print("Đường dẫn source_image không tồn tại!!!")

    CheckCrop_ = CheckCrop()
    preprocess = CheckCrop_.crop_or_not(source_image)
    print(preprocess)
    
    result = sad_talker.test(source_image, driven_audio, preprocess)

    return result
    

if __name__ == "__main__":
    demo = sadtalker_demo()
    print(demo)

