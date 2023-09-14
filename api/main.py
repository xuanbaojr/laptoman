import os
from src.inference import SadTalker
def sadtalker_demo(source_image, driven_audio, checkpoint_path='checkpoints', config_path='src/config', warpfn=None):
    sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)

    if os.path.exists(source_image):
        print("Source_image is exits!")
    else:
        print("Source_image is not exits!")

    preprocess = "full"    
    result = sad_talker.test(source_image, driven_audio, preprocess, still_mode = True, use_enhancer = False)
    return result
    

if __name__ == "__main__":

    source_image = './s/art_0.jpg'
    driven_audio = 's/bus_chinese_out.wav'
    demo = sadtalker_demo(source_image, driven_audio)
    print(demo)

# sinh -> chu dong sinh ko background