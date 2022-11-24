"""
Somewhat tracking cars for CNN labeling, need to improve this though, maybe remove noice and remove the flag pole
Also take only center coordinate for each car for labeling
"""

import cv2
from utils.video_decoding import VideoDecoder
import numpy as np
from numpy.lib.stride_tricks import as_strided
import time

video_data = VideoDecoder("../data_gather/cctv_data/output_12_31_11.mp4")


def pool2d(A, kernel_size, stride, padding=0, pool_mode='max'):
    """
     2D Pooling

     Parameters:
         A: input 2D array
         kernel_size: int, the size of the window over which we take pool
         stride: int, the stride of the window
         padding: int, implicit zero paddings on both sides of the input
         pool_mode: string, 'max' or 'avg'
     """
    # Padding
    A = np.pad(A, padding, mode='constant')

    # Window view of A
    output_shape = ((A.shape[0] - kernel_size) // stride + 1,
                    (A.shape[1] - kernel_size) // stride + 1)

    shape_w = (output_shape[0], output_shape[1], kernel_size, kernel_size)
    strides_w = (stride * A.strides[0], stride * A.strides[1], A.strides[0], A.strides[1])

    A_w = as_strided(A, shape_w, strides_w)

    # Return the result of pooling
    if pool_mode == 'max':
        return A_w.max(axis=(2, 3))
    elif pool_mode == 'avg':
        return A_w.mean(axis=(2, 3))


def save_coordinates_for_frame(coordinates, frame_number):
    with open(f"{video_data.video_name}_coordinates.txt", "a") as f:
        f.write(f"{frame_number}: {coordinates}")
        f.write("\n")


def get_pic(current_frame, previous_frame):
    kernel = 30

    diff = cv2.absdiff(current_frame, previous_frame)
    new_frame = np.zeros((diff.shape[0], diff.shape[1]))
    new_frame[diff > 40] = 255
    # new_frame[diff > 10] = 255
    with_noise = new_frame.copy()

    original_frame = video_data.current_frame
    color = (255, 0, 0)
    thickness = 2

    # trying to prevent tha tno 2 retangles are drawn on the same car
    rectangle_coordinates = []

    # print(new_frame.shape)
    for i in range(int(new_frame.shape[0] / kernel)):
        for j in range(int(new_frame.shape[1] / kernel)):
            # print(f"x-range: {i * kernel} - {(i + 1) * kernel} y-range: {j * kernel} - {(j + 1) * kernel}")
            # print("-"*50)
            if np.sum(new_frame[i * kernel:(i + 1) * kernel, j * kernel:(j + 1) * kernel]) < 100:
                new_frame[i * kernel:(i + 1) * kernel, j * kernel:(j + 1) * kernel] = 0

            if np.sum(new_frame[i * kernel:(i + 1) * kernel, j * kernel:(j + 1) * kernel]) > 100:
                kernel_top_left = (j * kernel, i * kernel)
                kernel_bottom_right = ((j + 1) * kernel, (i + 1) * kernel)
                kernel_middle = ((kernel_top_left[0] + kernel_bottom_right[0]) // 2,
                                 (kernel_top_left[1] + kernel_bottom_right[1]) // 2)

                # check if the rectangle is already drawn in close surroundings
                if not any([kernel_top_left[0] - kernel * 2 < x[0] < kernel_top_left[0] + kernel * 2 and kernel_top_left[1] - kernel * 2 < x[1] < kernel_top_left[1] + kernel * 2 for x in rectangle_coordinates]):
                    cv2.rectangle(original_frame, kernel_top_left, kernel_bottom_right, color, thickness)
                    rectangle_coordinates.append((kernel_middle[0], kernel_middle[1]))

                """# check if there are neighbour rectangles and if so combine them
                for x in rectangle_coordinates:
                    for y in rectangle_coordinates:
                        if x[0] - kernel * 10 < y[0] < x[0] + kernel * 10 and x[1] - kernel * 10 < y[1] < x[1] + kernel * 10:
                            rectangle_coordinates.remove(y)
                            rectangle_coordinates.append(((x[0] + y[0]) // 2, (x[1] + y[1]) // 2))

    # draw the rectangles
    for x in rectangle_coordinates:
        cv2.rectangle(original_frame, (x[0] - kernel // 2, x[1] - kernel // 2), (x[0] + kernel // 2, x[1] + kernel // 2), color, thickness)"""

    cv2.putText(original_frame, f"Number of cars: {len(rectangle_coordinates)}", (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(original_frame, f"Frame: {video_data.current_frame_number}", (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    # save_coordinates_for_frame(rectangle_coordinates, video_data.current_frame_number)

    return new_frame, with_noise, original_frame


def main():
    previous_frame = video_data.current_frame
    previous_frame = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

    while video_data.current_frame is not None:
        video_data.next_frame()
        current_frame = video_data.current_frame
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        frame, with_noise, original_frame = get_pic(current_frame, previous_frame)
        cv2.imshow("Original", original_frame)
        cv2.imshow("With_noise", with_noise)
        cv2.imshow("Without_Noise", frame)
        previous_frame = current_frame

        # time.sleep(0.02)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_data.video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
