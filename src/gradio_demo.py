import torch, uuid
import os, sys, shutil
from src.utils.preprocess import CropAndExtract
from src.test_audio2coeff import Audio2Coeff  
from src.facerender.animate import AnimateFromCoeff
from src.generate_batch import get_data
from src.generate_facerender_batch import get_facerender_data

from src.utils.init_path import init_path
from src.check_crop import CheckCrop


from pydub import AudioSegment


def mp3_to_wav(mp3_filename,wav_filename,frame_rate):
    mp3_file = AudioSegment.from_file(file=mp3_filename)
    mp3_file.set_frame_rate(frame_rate).export(wav_filename,format="wav")


class SadTalker():

    def __init__(self, checkpoint_path='checkpoints', config_path='src/config', lazy_load=False):

        if torch.cuda.is_available() :
            device = "cuda"
        else:
            device = "cpu"
        
        self.device = device

        os.environ['TORCH_HOME']= checkpoint_path

        self.checkpoint_path = checkpoint_path
        self.config_path = config_path
      
    def test(self, source_image, driven_audio, preprocess,
        still_mode=False,  use_enhancer=False, batch_size=1, size=256, 
        pose_style = 0, exp_scale=1.0, 
        use_ref_video = False,
        ref_video = None,
        ref_info = None,
        use_idle_mode = False,
        length_of_audio = 0, use_blink=True,
        result_dir='./results/'):

       
        self.sadtalker_paths = init_path(self.checkpoint_path, self.config_path, size, False, preprocess)
        print(self.sadtalker_paths)

        self.audio_to_coeff = Audio2Coeff(self.sadtalker_paths, self.device)
        self.preprocess_model = CropAndExtract(self.sadtalker_paths, self.device)
        self.animate_from_coeff = AnimateFromCoeff(self.sadtalker_paths, self.device)

        self.pre_image = CheckCrop()

        # pic_path - ok
            #time_tag ?
        time_tag = str(uuid.uuid4())
        save_dir = os.path.join(result_dir, time_tag)
        os.makedirs(save_dir, exist_ok=True)
        input_dir = os.path.join(save_dir, 'input')
        os.makedirs(input_dir, exist_ok=True)
        print(source_image)
            #chuyen anh folder goc qua result/timetag/input/source_image.png
        pic_path = os.path.join(input_dir, os.path.basename(source_image)) 
        shutil.move(source_image, input_dir)

         # audio_path
        if driven_audio is not None and os.path.isfile(driven_audio):
            audio_path = os.path.join(input_dir, os.path.basename(driven_audio))  

            #### mp3 to wav
            if '.mp3' in audio_path:
                mp3_to_wav(driven_audio, audio_path.replace('.mp3', '.wav'), 16000)
                audio_path = audio_path.replace('.mp3', '.wav')
            else:
                shutil.move(driven_audio, input_dir)

        # first_frame_dir - ok
        first_frame_dir = os.path.join(save_dir, 'first_frame_dir')
        os.makedirs(first_frame_dir, exist_ok=True)
            #results/time_tag/first_frame_dir ( art_0.mat, art_0.png, art_0_landmarks.txt )

        # preprocess - tim hieu ve crop
            # crop - cat anh ?
            # preprocess = 'crop' - khong co cung duoc ?

        # size - 256
        
        #first_coeff_path (b0, p0)
        preprocess_ = self.pre_image.crop_or_not(pic_path)
        
        first_coeff_path, crop_pic_path, crop_info = self.preprocess_model.generate(pic_path, first_frame_dir, preprocess, True, size)
        #
        batch = get_data(first_coeff_path, audio_path, self.device, ref_eyeblink_coeff_path=None, still=still_mode, idlemode=use_idle_mode, length_of_audio=length_of_audio, use_blink=use_blink) # longer audio?
        coeff_path = self.audio_to_coeff.generate(batch, save_dir, pose_style, ref_pose_coeff_path=None)
        #
        data = get_facerender_data(coeff_path, crop_pic_path, first_coeff_path, audio_path, batch_size, still_mode=still_mode, preprocess=preprocess, size=size, expression_scale = exp_scale)
        return_path = self.animate_from_coeff.generate(data, save_dir,  pic_path, crop_info, enhancer='gfpgan' if use_enhancer else None, preprocess=preprocess, img_size=size)
        return preprocess, return_path