# Import built-in libraries
import multiprocessing
import time
from multiprocessing import shared_memory
import os

# import downloaded packages
import PySimpleGUI as sg
import cv2
import numpy as np
from mss import mss

# import my own functions
from my_utils.screen_region import main

# Import deep learning library --> needed for object detection
import torch


def screen_recorder(path: str, filename: str, save: bool, position, width, height, detection, model_name):
    """
    Screen recording function, supports recording a specific region of the screen and multiprocessing.

    Parameters
        path: str
            Path to the folder where the video will be saved
        filename: str
            Name of the file to save the video as

    Returns
        None
    """
    # Configs
    debug = False  # Debug mode
    # width = 1500  # Width of the screen
    # height = 800  # Height of the screen0
    # position = (100, 0)  # Position of the screen
    fps = 15  # Frames per second
    frames_captured = 0  # Number of frames captured
    recording_start = time.time()  # Time when recording started
    frames_per_second = 0  # Frames per second
    new_fps = 0  # New frames per second for counting frames per second
    timer = time.time()  # Start timer
    timestamp = time.time()  # Timestamp for saving the video
    timeout = 1 / (fps * 2)  # Timeout for the while loop
    stop_record_shm = shared_memory.SharedMemory(name="screen_recording_running")  # 0 = stop running, 1 = running

    # If detection is enabled, loads the model here and saves it into models directory
    if detection:
        # Load model
        # check that models directory exists, if not create one
        if not os.path.exists("models"):
            os.mkdir("models")
        os.chdir("models")
        model = torch.hub.load('ultralytics/yolov5', model_name)
        os.chdir("..")

    # if save is true, create the video writer
    if save:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename=f'{path}/{filename}.mp4', fourcc=fourcc,
                              fps=fps,
                              frameSize=(width, height))

    bounding_box = {'top': position[0], 'left': position[1], 'width': width, 'height': height}

    # using mss, taking screenshots of the screen, and showing those images as a video with cv2
    with mss() as sct:
        while True:
            if (time.time() - timestamp) < timeout:
                continue
            if time.time() - timer < 1:
                new_fps += 1
            else:
                frames_per_second = new_fps
                new_fps = 0
                timer = time.time()
            sct_img = sct.grab(bounding_box)
            frame = np.array(sct_img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # If detection is enabled, runs the detection here
            if detection:
                # Prepare frame for detection
                frame_to_model = cv2.resize(frame, (244, 244))
                frame_to_model = cv2.cvtColor(frame_to_model, cv2.COLOR_BGR2RGB)

                # Inference
                results = model(frame_to_model)
                # Results
                results = results.pandas().xyxy[0]  # img1 predictions (pandas)

                # Get confidence threshold from GUI
                conf_threshold = shared_memory.SharedMemory(name='confidence_threshold')

                # Draw bounding boxes
                for i in range(len(results)):
                    x1, y1, x2, y2, conf, class_id, class_name = results.iloc[i].values

                    conf = round(conf * 100, 0)
                    if conf < conf_threshold.buf[0]:
                        continue

                    x1 = int(x1 * (width / 244))
                    y1 = int(y1 * (height / 244))
                    x2 = int(x2 * (width / 244))
                    y2 = int(y2 * (height / 244))

                    # print(x1, y1, x2, y2, conf, class_id, class_name)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, f"{class_name} {conf}%", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # If save is true, write the frame to the video
            if save:
                cv2.imshow('screen', frame)
                out.write(frame)
            else:
                cv2.imshow('screen', frame)

            # If debug is true, additional information is shown
            if debug:
                print(f"[INFO] Capture time: {round(time.time() - recording_start, 3)} seconds,", end=" ")
                print(f"Frames per second: {frames_per_second},", end=" ")
                print(f"Total frames captured: {frames_captured}", end=" ")
                print(f"Frame shape: {frame.shape}")

            # if users presses q or stop recording button is pressed, stop recording
            if (cv2.waitKey(1) & 0xFF) == ord('q') or stop_record_shm.buf[0] == 0:
                if save:
                    out.release()
                cv2.destroyAllWindows()
                break
            frames_captured += 1
            timestamp = time.time()

    # information for the main script back from this child process that it was closed normally
    stop_record_shm.buf[1] = 1


def open_window():
    layout = [
        [sg.Text('Enter the name of the file to save:'), sg.InputText(default_text="test")],
        [
            sg.Text("Choose save location:"),
            sg.InputText(default_text="Add a path here"),
            sg.FolderBrowse(),
            sg.Checkbox("Save file", default=False)],
        [
            sg.Button('Start recording'),
            sg.Button("Stop recording"),
            sg.Button("Choose region"),
            sg.Checkbox("Object detection", default=False),
            sg.OptionMenu(["yolov5s", "yolov5m", "yolov5l", "yolov5x"], default_value="yolov5s", key="model"),
            sg.Slider(range=(0, 100), default_value=50, orientation="h", size=(20, 15), key="confidence",
                      tooltip="Confidence threshold", enable_events=True),
        ]
    ]

    window = sg.Window('Screen recorder', layout)

    # Default values for recording if no region is selected
    position = (0, 0)
    width = 800
    height = 800

    #########################
    # values[1] = path - str
    # values[0] = filename - str
    # values[2] = save - BOOLEAN
    # values[3] = object_detection - BOOLEAN
    #########################
    while True:
        event, values = window.read()
        print(f"Events: {event}")
        print(f"Values: {values}")

        # print(record_running.buf[0])
        if event == sg.WIN_CLOSED:
            break

        record_running = shared_memory.SharedMemory(name='screen_recording_running')
        conf_threshold = shared_memory.SharedMemory(name='confidence_threshold')

        if event == 'Start recording' and record_running.buf[0] == 0:
            record_running.buf[0] = 1  # Setting the shared memory to 1 to start recording

            # Opening screen recording in a child process
            p1 = multiprocessing.Process(target=screen_recorder,
                                         args=(values[1],
                                               values[0],
                                               values[2],
                                               position,
                                               width,
                                               height,
                                               values[3],
                                               values["model"],))
            p1.start()
        elif event == 'Start recording' and record_running.buf[0] == 1:
            print("[WARNING] Recording already running")

        # Choose region here by calling my util function from my other script, this also opened as a child process
        if event == 'Choose region' and record_running.buf[0] == 0:
            queue = multiprocessing.Queue()
            p2 = multiprocessing.Process(target=main, args=(queue,))
            p2.start()
            coordinates = queue.get()
            # print(coordinates)
            p2.join()
            if len(coordinates[0]) == 2 and len(coordinates[1]) == 2:
                position = (coordinates[0][1], coordinates[0][0])
                width = coordinates[1][0] - coordinates[0][0]
                height = coordinates[1][1] - coordinates[0][1]
        elif event == 'Choose region' and record_running.buf[0] == 1:
            print("[WARNING] Recording already running, cannot choose region")

        # Stop recording here, checks if child process was stopped normally, if not force it to close
        if event == 'Stop recording' and record_running.buf[0] == 1:
            print("[INFO] Stopping recording")
            record_running.buf[0] = 0  # Setting the shared memory to 0 to stop recording
            terminate_time = time.time()
            while record_running.buf[1] != 1:
                if time.time() - terminate_time > 3:
                    print("[ERROR] Process was forcefully terminated")
                    print("[ERROR] Something went wrong stopping the recording process!")
                    p1.terminate()
                    record_running.buf[1] = 0
                    break
                time.sleep(1)
            if record_running.buf[1] == 1:
                p1.join()
                record_running.buf[1] = 0
                print("[INFO] Closed recording subprocess succesfully")
        elif event == 'Stop recording' and record_running.buf[0] == 0:
            print("[WARNING] Recording not running")

        # Event for the confidence slider that is then passed into memory for child process(object detection) to use
        if event == "confidence":
            conf_threshold.buf[0] = int(values["confidence"])
            print(f"Confidence threshold: {values['confidence']}")

    window.close()


if __name__ == '__main__':
    # Creating shared memory for the child process to use
    try:
        shm = shared_memory.SharedMemory(name='screen_recording_running', create=True, size=2)
    except FileExistsError:
        shm = shared_memory.SharedMemory(name='screen_recording_running', create=False, size=2)
    try:
        conf_thres = shared_memory.SharedMemory(name='confidence_threshold', create=True, size=1)
    except FileExistsError:
        conf_thres = shared_memory.SharedMemory(name='confidence_threshold', create=False, size=1)

    # Adding default values to shared memory
    shm.buf[0] = 0  # to tell subprocess to stop running
    shm.buf[1] = 0  # confirmation that subprocess did stop running
    conf_thres.buf[0] = 50   # confidence threshold

    # Opening the main window, MAIN PROCESS
    open_window()

    # Closing shared memories
    shm.unlink()
    conf_thres.unlink()
