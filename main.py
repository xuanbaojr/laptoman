import os
from src.gradio_demo import SadTalker
# warpfn , lazy_load ?
def sadtalker_demo(source_image, driven_audio, checkpoint_path='checkpoints', config_path='src/config', warpfn=None):
    sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)
    # source image :


    if os.path.exists(source_image):
        print("Source_image is exits!")
    else:
        print("Source_image is not exits!")

    preprocess = "full"
    print(preprocess)
    
    result = sad_talker.test(source_image, driven_audio, preprocess)

    return result
    

if __name__ == "__main__":
    source_image = 'test/test.jpg'
    driven_audio = 'test/bus_chinese.wav'
    demo = sadtalker_demo(source_image, driven_audio)
    print(demo)

