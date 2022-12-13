import os
import time
import datetime as dt


def read_file_content(path):  # Get labels and return them as a string after remove file
    try:
        with open(path, "r") as f:
            content = f.read()
            return content
    except FileNotFoundError:
        print("File not found")
        return ""


def change_dir():
    folder_name = "exp5"

    # Accessing the folder with labels
    cwd = os.getcwd()
    cwd = cwd.split("\\")[:-1]
    cwd = "\\".join(cwd) + f"\\data\\with_ai\\{folder_name}\\labels"
    os.chdir(cwd)


def read_labels():  # Counting the number of files in the folder
    files = os.listdir()
    print(f"Number of files: {len(files)}")

    labels = []
    # car_counter = 0

    # Reading the content of the first file
    for file in files:
        content = read_file_content(file)
        if content == "":
            continue
        content = content.split("\n")
        content = [x for x in content if x != ""]
        # car_counter += len(content)
        labels.append(content)
        os.remove(file)

    # print(labels)
    # print(f"[INFO] Cars counted: {car_counter}")
    return labels


def check_if_car_moving(labels, car_locations=None):  # Takes 10 frames of video data and check if the car is moving

    new_cars_in_frame = 0

    if car_locations is None:
        car_locations = {}

    if car_locations is None:
        car_locations = {}
    for label in labels:
        for car in label:
            next_car_id = len(car_locations.keys()) + 1

            info = car.split(" ")
            x = float(info[1])
            y = float(info[2])

            # check if car is in dictionary using x and y and their absolute difference
            # if not, add it to the dictionary
            car_to_add = []
            car_to_be_added = True
            for key, value in car_locations.items():
                dict_car_x = value["x"]
                dict_car_y = value["y"]
                if abs(x - dict_car_x) < 0.03 and abs(y - dict_car_y) < 0.03:
                    car_to_be_added = False
                    car_locations[key]["x"] = x
                    car_locations[key]["y"] = y
                    car_locations[key]["updated"] = dt.datetime.now()
                    break
            else:
                if car_to_be_added:
                    car_to_add = [next_car_id, x, y]
                    new_cars_in_frame += 1  # Adding new car to counter

            # add new cars
            if car_to_add:
                car_locations[car_to_add[0]] = {"x": car_to_add[1], "y": car_to_add[2], "updated": dt.datetime.now()}

    # Remove cars that have not been seen in one second
    current_time = dt.datetime.now()
    keys_to_remove = []
    for key, value in car_locations.items():
        if (current_time - value["updated"]).total_seconds() > 2:
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del car_locations[key]

    # Returning dictionary with cars and their locations so next iteration can check if they are movingq
    if new_cars_in_frame > 10:
        new_cars_in_frame = 1
    return car_locations, new_cars_in_frame


def count_cars():
    # read_folder_content()
    starting_time = time.time()
    car_locations = None
    total_cars_counter = 0

    while True:
        print("[INFO] Counting cars...")
        labels = read_labels()
        batch_size = 10
        batches = len(labels) // batch_size

        for i in range(batches):
            if i != batches - 1:
                batch = labels[i * batch_size:(i + 1) * batch_size]
            else:
                batch = labels[i * batch_size:]

            car_locations, new_cars = check_if_car_moving(batch, car_locations)
            total_cars_counter += new_cars

            for key, value in car_locations.items():
                # print(f"Car {key}: {value}")
                pass

        print(f"[INFO] Batches: {batches}")
        print(f"[INFO] Cars counted")
        print(f"[INFO] Total cars counted: {total_cars_counter}")
        print(f"[INFO] Sleeping for 1 seconds...")
        time.sleep(1)
        os.system("cls")


def main():
    # Change to right directory
    change_dir()

    # Count new cars in video
    count_cars()


if __name__ == '__main__':
    main()
