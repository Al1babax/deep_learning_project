import os


def main():
    os.system('call "C:/Users/Alibaba/Desktop/data stuff/torch_gpu_test/Scripts/activate.bat"')
    os.system('ECHO "Activating virtual environment"')
    os.chdir('C:/Users/Alibaba/Desktop/deep_learning_project/deep_learning_project/count_cars')
    os.system('py object_tracker.py')
    os.system('timeout /t -1')


if __name__ == "__main__":
    main()
