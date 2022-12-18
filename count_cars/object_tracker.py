import cv2
import numpy as np
import pandas as pd
import torch
import time
import logging
import os

# Starting logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(name)s|%(levelname)s|%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filename='data/log.txt')


# Video decoder --> making video frame to numpy array
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

    def next_frame(self):  # Read next frame
        ret, frame = self.video.read()
        self.current_frame = frame
        self.current_frame_number += 1

    def show_frame(self):  # Show current frame
        cv2.imshow('frame', self.current_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def draw_boxes(frame, boxes):
    # Drawing all the bounding boxes
    for box in boxes:
        cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)


def parse_detection_results(results, frame):
    """
    Parsing through all the results and counting cars that are in the right area.
    :param results:
    :param frame:
    :return:
    """
    global car_counter
    global temporal_memory

    # filter confidence
    results = results[results['confidence'] > 0.7]
    # filter class
    results = results[results['class'] == 0]  # 0 if I trained the model
    # results = results[results['class'] == 2] for pretrained COCO model

    results['x_center'] = (results['xmin'] + results['xmax']) / 2
    results['y_center'] = (results['ymin'] + results['ymax']) / 2

    # draw boxes
    draw_boxes(frame, results[['xmin', 'ymin', 'xmax', 'ymax']].values)

    results = results[(results['y_center'] <= 255) & (results["y_center"] >= 254) & (results['x_center'] > 0) & (
            results['x_center'] < 300)]
    new_results = results

    if temporal_memory.shape[0] != 0:
        # print(temporal_memory)
        # take all the x_center values from temporal_memory dataframe
        y_center_values = temporal_memory['y_center'].values

        # remove all rows from results whose x_center value is within 0.1% of any x_center value in x_center_values
        new_results = pd.DataFrame(columns=results.columns)

        for i in range(results.shape[0]):
            # Checking that new car is not in the same place as old car aka same car
            if np.any(np.abs(results.iloc[i]['y_center'] - y_center_values) > 3):
                new_row = results.iloc[i]
                new_results = pd.concat([new_results, new_row], axis=1)
            else:
                print("Duplicate detected")

        temporal_memory = pd.DataFrame(columns=temporal_memory.columns)

    # Logging the new cars for API
    if len(new_results) > 0:
        logging.info(f"New car detected, Total cars: {car_counter + 1}")
        print(new_results)

    # for each result left increase counter
    results_count = new_results['y_center'].count()
    car_counter += results_count

    # save results to temporal memory
    temporal_memory = new_results

    # Returning boolean value whether the frame should be saved or not
    if len(new_results) > 0:
        return True
    else:
        return False


def test_video(video_show=False):
    # Main loop that is going through all the frames
    while True:
        frame = video_c.current_frame
        results = model(video_c.current_frame)
        results = results.pandas().xyxy[0]  # img1 predictions (pandas)
        save_frame = parse_detection_results(results, frame)

        # Draw area of detection
        cv2.polylines(frame, [np.array([[0, 400], [220, 250], [50, 260], [0, 280]])], True, (0, 0, 255), 2)
        # Draw horizontal line of detection
        cv2.line(frame, (0, 255), (640, 255), (255, 0, 0), 3)
        # Draw a vertical limit that no car right to this will we counted
        cv2.line(frame, (300, 0), (300, 480), (255, 0, 0), 3)
        # Draw text for car count
        cv2.putText(frame, "Cars: " + str(car_counter), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Showing the frame
        if video_show:
            cv2.imshow('frame', frame)

        # Going to next frame
        video_c.next_frame()
        # time.sleep(0.1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


def live_video(video_show=False):
    cap = cv2.VideoCapture('http://webcam.teuva.fi/axis-cgi/mjpg/video.cgi')
    while True:
        ret, frame = cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = model(frame)
            results = results.pandas().xyxy[0]  # img1 predictions (pandas)
            save_frame = parse_detection_results(results, frame)

            # Draw area of detection
            cv2.polylines(frame, [np.array([[0, 400], [220, 250], [50, 260], [0, 280]])], True, (0, 0, 255), 2)
            # Draw horizontal line of detection
            cv2.line(frame, (0, 255), (640, 255), (255, 0, 0), 3)
            # Draw a vertical limit that no car right to this will we counted
            cv2.line(frame, (300, 0), (300, 480), (255, 0, 0), 3)
            # Draw text for car count
            cv2.putText(frame, "Cars: " + str(car_counter), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if video_show:
                cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main(video="test", video_show=False):
    if video == "test":
        test_video(video_show)
    if video == "live":
        live_video(video_show)


if __name__ == '__main__':
    mode = "live"

    # Timer for measuring the time of the script
    start_time = time.time()

    # Clean log file --> THIS IS ONLY FOR TESTING
    with open('data/log.txt', 'w') as f:
        f.truncate()
        # pass

    if not os.path.exists('models/best.pt'):
        model = torch.hub.load('ultralytics/yolov5', 'yolov5x',
                               pretrained=True)  # load YOLOv5s model, with COCO pretrained weights
    else:
        model = torch.hub.load('ultralytics/yolov5', 'custom',
                               path="models/best.pt")  # load YOLOv5s model, with my custom weights

    if os.path.exists("../data_gather/cctv_data/output_14_35_03.mp4"):
        mode = "test"
        video_c = VideoDecoder("../data_gather/cctv_data/output_14_35_03.mp4")

    # video_c = VideoDecoder("../data_gather/cctv_data/output_15_45_13.mp4")

    # Init car counter to 0
    car_counter = 0
    # Create temporal memory to store the cars that are already counted
    temporal_memory = pd.DataFrame()

    # Change the mode parameter to "test" if you want to run test video in local directory
    main(mode, video_show=True)
