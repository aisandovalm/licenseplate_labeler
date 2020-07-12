import time
import ffmpy
import os

def convert(inputted_file, output_dir='tmp'):
    if 'MP4' in inputted_file:
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        current_time = time.strftime("%Y%m%d-%H%M%S")
        video_name = os.path.join(output_dir, str(current_time) + ".avi")
        ff = ffmpy.FFmpeg(
            inputs={inputted_file : None}, outputs={video_name: "-filter:v 'setpts=0.5*PTS' -q:v 1 -c:a mp3 -c:v mpeg4"},
            global_options="-loglevel warning")#'-vf select='not(mod(n\,100))' -c:a mp3 -c:v mpeg4'
        ff.cmd
        ff.run()
    else:
        video_name = inputted_file
    return video_name