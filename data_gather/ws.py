import cv2
import time
import datetime as dt

# Configs
DEBUG = False
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(f'cctv_data/output_{dt.datetime.now().strftime("%H_%M_%S")}.mp4', fourcc, 20.0, (640, 480))
cap = cv2.VideoCapture('http://webcam.teuva.fi/axis-cgi/mjpg/video.cgi')

# Variables for script
frames_captured = 0  # Number of frames captured
recording_start = time.time()  # Time when recording started
frames_per_second = 0  # Frames per second
new_fps = 0  # New frames per second for counting frames per second
timer = time.time()  # Start timer

recording_fps = 2  # Frames per second


def record_video():
    global frames_captured, recording_start, frames_per_second, new_fps, timer, out
    while True:
        ret, frame = cap.read()
        if time.time() - timer < 1:
            new_fps += 1
        else:
            frames_per_second = new_fps
            new_fps = 0
            timer = time.time()

        if ret:
            if DEBUG:
                print(f"[INFO]Capture time: {round(time.time() - recording_start, 3)} seconds,", end=" ")
                print(f"Frames per second: {frames_per_second},", end=" ")
                print(f"Total frames captured: {frames_captured}", end=" ")
                print(f"Frame shape: {frame.shape}")

            cv2.imshow("Capturing", frame)
            frames_captured += 1
            out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # time.sleep(1 / recording_fps)

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def main():
    starting_time = time.time()
    print("[INFO]Starting video capture...")
    record_video()
    print(f"[INFO]Video capture finished in {round(time.time() - starting_time, 3)} seconds")
    print(f"[INFO]Video saved as output_{dt.datetime.now().strftime('%H_%M_%S')}.mp4")


if __name__ == '__main__':
    main()
