import cv2

class FrameByFrame:
    def __init__(self, video_source=0):
        self.video_path = video_source
        self.frame_count = 0

        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)


    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            self.frame_count = self.frame_count + 1
            #print('frame: {}'.format(self.frame_count))
            if ret:
                # Return a boolean success flag and the current frame converted to RGB
                return (ret, frame)
            else:
                print('Se llegó al final del video')
                return (ret, None)
        else:
            return (ret, None)