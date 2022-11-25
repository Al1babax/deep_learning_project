import datetime as dt
import multiprocessing
import time
from multiprocessing import shared_memory

import PySimpleGUI as sg
import cv2
import numpy as np
from mss import mss

from my_utils.screen_region import region, main
from yolov5_detect import run_predict


def screen_recorder(path: str, filename: str, save: bool, position, width, height, object_detection: bool):
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
    # height = 800  # Height of the screen
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

    if save:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename=f'{path}/{filename}.mp4', fourcc=fourcc,
                              fps=fps,
                              frameSize=(width, height))

    bounding_box = {'top': position[0], 'left': position[1], 'width': width, 'height': height}

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
            if save:
                cv2.imshow('screen', frame)
                out.write(frame)
            else:
                cv2.imshow('screen', frame)
            if debug:
                print(f"[INFO] Capture time: {round(time.time() - recording_start, 3)} seconds,", end=" ")
                print(f"Frames per second: {frames_per_second},", end=" ")
                print(f"Total frames captured: {frames_captured}", end=" ")
                print(f"Frame shape: {frame.shape}")
            if (cv2.waitKey(1) & 0xFF) == ord('q') or stop_record_shm.buf[0] == 0:
                if save:
                    out.release()
                cv2.destroyAllWindows()
                break
            frames_captured += 1
            timestamp = time.time()

    stop_record_shm.buf[1] = 1


def object_detection(path: str, filename: str):
    # full_path = f'{path}/{filename}_{dt.datetime.now().strftime("%H_%M_%S")}.mp4'
    full_path = f'{path}/{filename}.mp4'
    run_predict(full_path)


def open_window():
    layout = [
        [sg.Text('Enter the name of the file to save:'), sg.InputText(default_text="test")],
        [
            sg.Text("Choose save location:"),
            sg.InputText(default_text="C:/Users/Alibaba/Desktop/deep_learning_project/deep_learning_project/data"),
            sg.FolderBrowse(),
            sg.Checkbox("Save file", default=False)],
        [
            sg.Button('Start recording'),
            sg.Button("Stop recording"),
            sg.Button("Choose region"),
            sg.Checkbox("Object detection", default=False)
        ]
    ]

    window = sg.Window('Screen recorder', layout)

    # Default values for recording if no region is selected
    position = (100, 0)
    width = 1500
    height = 800

    while True:
        event, values = window.read()
        print(event, values)
        record_running = shared_memory.SharedMemory(name='screen_recording_running')
        # print(record_running.buf[0])
        if event == sg.WIN_CLOSED:
            break

        if event == 'Start recording' and record_running.buf[0] == 0:
            record_running.buf[0] = 1  # Setting the shared memory to 1 to start recording
            # values[1] = path
            # values[0] = filename
            # values[2] = save - BOOLEAN
            # values[3] = object_detection - BOOLEAN
            p1 = multiprocessing.Process(target=screen_recorder,
                                         args=(values[1], values[0], values[2], position, width, height, values[3]))
            p1.start()
        elif event == 'Start recording' and record_running.buf[0] == 1:
            print("[WARNING] Recording already running")

        if event == 'Choose region' and record_running.buf[0] == 0:
            queue = multiprocessing.Queue()
            p2 = multiprocessing.Process(target=main, args=(queue,))
            p2.start()
            coordinates = queue.get()
            # print(coordinates)
            p2.join()
            position = (coordinates[0][1], coordinates[0][0])
            width = coordinates[1][0] - coordinates[0][0]
            height = coordinates[1][1] - coordinates[0][1]
        elif event == 'Choose region' and record_running.buf[0] == 1:
            print("[WARNING] Recording already running, cannot choose region")

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

                if values[3] is True:
                    print("[INFO] Starting object detection")
                    object_detection(values[1], values[0])
                    print("[INFO] Object detection finished")

        elif event == 'Stop recording' and record_running.buf[0] == 0:
            print("[WARNING] Recording not running")

    window.close()


def draw_rectangle():  # TODO - Fix the rectangle not being drawn correctly
    pass


if __name__ == '__main__':
    shm = shared_memory.SharedMemory(name='screen_recording_running', create=True, size=2)
    shm.buf[0] = 0  # to tell subprocess to stop running
    shm.buf[1] = 0  # confirmation that subprocess did stop running
    open_window()
