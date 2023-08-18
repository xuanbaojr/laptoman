import os
from src.gradio_demo import SadTalker

# warpfn , lazy_load ?
def sadtalker_demo(checkpoint_path='checkpoints', config_path='src/config', warpfn=None):
    sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)
    # source image :
    source_image = 'test/art_0.png'
    driven_audio = 'test/deyu.wav'

    if os.path.exists(source_image):
        print("Đường dẫn source_image đúng!")
    else:
        print("Đường dẫn source_image không tồn tại!!!")
    
    result = sad_talker.test(source_image, driven_audio)

    return result
    

if __name__ == "__main__":
    demo = sadtalker_demo()
    print(demo)

