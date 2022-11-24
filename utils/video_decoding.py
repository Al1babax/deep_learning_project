import cv2


class VideoDecoder:

    def __init__(self, video_path):
        self.video_path = video_path
        self.video = cv2.VideoCapture(self.video_path)  # Open video file
        self.current_frame_number = 0
        self.video_name = video_path.split("/")[-1]

        # Making sure the video is opened
        if not self.video.isOpened():
            print("Error opening video stream or file")
            exit(1)

        # Read first frame
        ret, frame = self.video.read()
        self.current_frame = frame

    def next_frame(self):   # Read next frame
        ret, frame = self.video.read()
        self.current_frame = frame
        self.current_frame_number += 1

    def show_frame(self):   # Show current frame
        cv2.imshow('frame', self.current_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
