import os


def main():
    python_path = "C:/Users/Alibaba/Desktop/data stuff/torch_gpu_test/Scripts/python.exe"
    os.chdir('C:/Users/Alibaba/Desktop/deep_learning_project/deep_learning_project/count_cars')
    os.system(f'"{python_path}" object_tracker.py')
    os.system('timeout /t -1')


if __name__ == "__main__":
    main()
