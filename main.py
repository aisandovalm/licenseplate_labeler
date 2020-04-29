from db_builder import DBBuilder
from frame_by_frame import FrameByFrame
from convert_video import convert
import cv2
import os, sys
import glob
import threading
from threading import Timer

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
    global prepareVideosThread, _DELAY, VIDEOS_LIST

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
                    print('boxes: {}'.format(bboxes))
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
            else:
                print('End of video')
                break
    except IndexError:
        print('List is empty')
    finally:
        if not prepareVideosThread.isAlive():
            print('Thread is not running. Closing process')
            return
        else:
            wait_time = 10
            print('Thread is running. Waiting {} seconds for the next video'.format(wait_time))
            Timer(wait_time, run_annotator).start()

if __name__ == "__main__":
    global prepareVideosThread
    #dbBuilder = DBBuilder(DIR_SOURCE_PATH, DIR_IMAGES_PATH)

    prepareVideosThread = threading.Thread(target=prepare_videos, args=(DIR_VIDEOS_PATH,))
    prepareVideosThread.start()

    run_annotator()

    print('Closing app')
    sys.exit()