import socket
import os


# Socket test to find what is my actual public IP4V address, using this to run the RestAPI
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def run_server():
    uvicorn_path = "C:/Users/Alibaba/Desktop/data stuff/torch_gpu_test/Scripts/uvicorn.exe"
    os.chdir("C:/Users/Alibaba/Desktop/deep_learning_project/deep_learning_project/API")
    os.system(f'"{uvicorn_path}" main:app --host {get_ip_address()} --port 3010 --reload')


def main():
    python_path = "C:/Users/Alibaba/Desktop/data stuff/torch_gpu_test/Scripts/python.exe"
    run_server()


if __name__ == "__main__":
    main()
