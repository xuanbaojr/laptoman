import cv2
import numpy as np
def paste_video(video_path_01, video_path_02):

    video_01 = cv2.VideoCapture(video_path_01)
    fps = 25
    frames_01 = []
    while 1:
        still_reading, frame = video_01.read()
        if not still_reading:
            video_01.release()
            break
        frames_01.append(frame)

    video_02 = cv2.VideoCapture(video_path_02)
    frames_02 = []
    while 1:
        still_reading, frame = video_02.read()
        if not still_reading:
            video_02.release()
            break
        frames_02.append(frame)
    frame_w = 256
    frame_h = 256

    face_h = int(158*1.2)
    face_w = int(114*1.2)

    tmp_path = 'test/test.mp4'
    out_tmp = cv2.VideoWriter(tmp_path, cv2.VideoWriter_fourcc(*'MP4V'), fps, (frame_w, frame_h))
    for key in range(len(frames_01)):
        frames_01[key] = cv2.resize(frames_01[key].astype(np.uint8), ((face_h),(face_w)))
        frames_02[key] = frames_02[key].astype(np.uint8)

        mask = 255*np.ones(frames_01[key].shape, dtype=np.uint8)
        location = (120,72)
        gen_video = cv2.seamlessClone(frames_01[key], frames_02[key], mask,
                                      location, cv2.NORMAL_CLONE)
        out_tmp.write(gen_video)

    out_tmp.release

    return "ok"

if __name__ == "__main__":
    print("hahaha")
    video_path_01 = 'test/head.mp4'
    video_path_02 = 'test/body.mp4'
    demo = paste_video(video_path_01, video_path_02)
    
    print(demo)
