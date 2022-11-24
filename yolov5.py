from yolov5 import detect
from yolov5 import export


def run_predict():
    weights = "yolov5x6.pt"
    video_path = "data_gather/cctv_data/output_12_31_11.mp4"
    stream = "http://webcam.teuva.fi/axis-cgi/mjpg/video.cgi"
    picture = "data_gather/test_image.jpeg"
    random_video = "data/test.mp4"
    conf_thres = 0.70
    iou_thres = 0.35
    device = "0"
    line_thickness = 2
    view_img = False
    vid_stride = 1

    detect.run(
        weights=weights,
        source=random_video,
        conf_thres=conf_thres,
        iou_thres=iou_thres,
        device=device,
        line_thickness=line_thickness,
        view_img=view_img,
        vid_stride=vid_stride,
    )


def export_model():
    weights = "yolov5s.pt"
    device = "cpu"
    keras = True
    include = ["saved_model"]

    export.run(
        weights=weights,
        device=device,
        keras=keras,
        include=include,
    )


run_predict()
