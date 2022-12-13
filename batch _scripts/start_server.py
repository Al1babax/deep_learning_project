import socket
import os


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def run_server():
    os.chdir("C:/Users/Alibaba/Desktop/deep_learning_project/deep_learning_project/API")
    os.system(f"uvicorn main:app --host {get_ip_address()} --port 3010 --reload")


def main():
    os.system('call "C:/Users/Alibaba/Desktop/data stuff/torch_gpu_test/Scripts/activate.bat"')
    os.system('ECHO "Activating virtual environment"')
    os.system('ECHO "Starting server"')
    run_server()


if __name__ == "__main__":
    main()
