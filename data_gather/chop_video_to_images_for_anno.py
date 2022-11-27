import cv2
import os


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


def chop_video_to_images_for_anno(video_path, output_path, frame_rate=20):
    video_decoder = VideoDecoder(video_path)
    video_decoder.next_frame()
    frame_number = 1
    while video_decoder.current_frame is not None:
        if frame_number % frame_rate == 0:
            cv2.imwrite(output_path + "/frame" + str(frame_number) + ".jpg", video_decoder.current_frame)
            print("Saved frame " + str(frame_number))
        video_decoder.next_frame()
        frame_number += 1

    print("Done chopping video to images for annotation")


if __name__ == "__main__":
    video_file_location = "cctv_data/output_12_31_11.mp4"
    # create folder for images
    output_path = "cctv_data/output_12_31_11"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    chop_video_to_images_for_anno(video_file_location, f"cctv_data/{video_file_location.split('/')[1].split('.')[0]}", 500)
