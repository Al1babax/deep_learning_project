from my_utils.yolov5.detect import run


def run_predict(
        source,  # This is the path to the video file
        weights="yolov5x6.pt",  # This is the path to the weights file
        conf_thres=0.75,  # Confidence threshold
        iou_thres=0.02,  # Density of bounding boxes
        device="0",  # Device to run on
        line_thickness=2,  # Thickness of bounding box lines
        view_img=False,  # Display results
        vid_stride=3,  # Number of frames to skip between detections
        save_location="C:/Users/Alibaba/Desktop/deep_learning_project/deep_learning_project/data/with_ai",    # Location to save the video
        save_text=True,  # Save the text file
        no_save=True,  # Don't save the video
):
    run(
        weights=weights,
        source=source,
        conf_thres=conf_thres,
        iou_thres=iou_thres,
        device=device,
        line_thickness=line_thickness,
        view_img=view_img,
        vid_stride=vid_stride,
        project=save_location,
        save_txt=save_text,
        nosave=no_save,
    )


if __name__ == '__main__':
    pic_source = "../data/test.mp4"
    live_stream = "http://webcam.teuva.fi/axis-cgi/mjpg/video.cgi"
    own_weights = "my_utils/yolov5/runs/train/exp6/weights/last.pt"
    run_predict(source=live_stream, view_img=True, weights=own_weights)
