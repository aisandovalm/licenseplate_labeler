from db_builder import DBBuilder
from frame_by_frame import FrameByFrame
from convert_video import convert
import cv2
import os, sys
import glob
import threading
from threading import Timer
import numpy as np

DIR_SOURCE_PATH = 'D:\Development\Big Data and Machine Learning\Patentes\dataset-gopro'
DIR_VIDEOS_PATH = os.path.join(DIR_SOURCE_PATH, 'videos')
DIR_IMAGES_PATH = os.path.join(DIR_SOURCE_PATH, 'images')

_DEFAULT_DELAY =  24
_DELAY = _DEFAULT_DELAY
VIDEOS_LIST = []

def prepare_videos(source):
    global VIDEOS_LIST
    for video_path in glob.glob(os.path.join(source, '*')):#'./tmp'
        print('Preparing video: {}'.format(video_path))
        video = convert(video_path)
        VIDEOS_LIST.append(video)

def run_annotator():
    global prepareVideosThread, _DELAY, VIDEOS_LIST, dbBuilder

    try:
        video_path = VIDEOS_LIST.pop(0)
    
        videoReader = FrameByFrame(video_path)

        while True:
            ok, frame = videoReader.get_frame()

            if ok:
                cv2.imshow("Annotator", frame)

                key = cv2.waitKey(_DELAY) & 0xff
                if key == 97: # a = make annotation
                    bboxes = cv2.selectROIs("Annotator", frame)
                    frame_bkp = np.copy(frame)

                    # draw boxes
                    for i, box in enumerate(bboxes):
                        p1 = (box[0], box[1])
                        p2 = (box[0]+box[2], box[1]+box[3])
                        cv2.rectangle(frame_bkp, p1, p2, (0,0,255))
                        cv2.putText(frame_bkp, 'n {}'.format(i), p1, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))
                    cv2.imshow("Annotator", frame_bkp)
                    key = cv2.waitKey(1)
                    
                    lpNumbers = []
                    for i, box in enumerate(bboxes):
                        lp_number = input('License plate number of lp={}: '.format(i))
                        lpNumbers.append(lp_number.upper())
                    
                    dbBuilder.write_line(frame, bboxes, lpNumbers)
                if key == 42: # *
                    _DELAY = _DEFAULT_DELAY
                    print(_DELAY)
                if key == 43: # +
                    delta = _DEFAULT_DELAY*0.1
                    _DELAY = int(max(1, _DELAY-delta))
                    print(_DELAY)
                if key == 45: # -
                    delta = _DEFAULT_DELAY*0.1
                    _DELAY = int(_DELAY+delta)
                    print(_DELAY)
                if key == 113: # q
                    return
            else:
                print('End of video')
                break
    except IndexError:
        #print('List is empty')
        pass
    finally:
        if (prepareVideosThread is not None) and (not prepareVideosThread.isAlive()):
            #print('Thread is not running. Closing process')
            return
        elif prepareVideosThread is None:
            return
        else:
            wait_time = 10
            #print('Thread is running. Waiting {} seconds for the next video'.format(wait_time))
            Timer(wait_time, run_annotator).start()

def generate_list():
    #VIDEOS_LIST.append('D:\\fiscalia\\video_test\\kauel.mp4')
    #VIDEOS_LIST.append('D:\\Development\\Big Data and Machine Learning\\Patentes\\dataset-gopro\\videos\\GOPR1310.MP4')
    VIDEOS_LIST.append('.\\tmp\\20200710-163416.avi')

if __name__ == "__main__":
    global prepareVideosThread, dbBuilder
    PREPARE_VIDEOS = True
    dbBuilder = DBBuilder(DIR_SOURCE_PATH, DIR_IMAGES_PATH)

    if PREPARE_VIDEOS:
        prepareVideosThread = threading.Thread(target=prepare_videos, args=(DIR_VIDEOS_PATH,))
        prepareVideosThread.start()
    else:
        prepareVideosThread = None
        generate_list()

    run_annotator()

    #print('Closing app')
    sys.exit()