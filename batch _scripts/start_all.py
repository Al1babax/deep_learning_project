import subprocess


def start_api():
    subprocess.Popen(["python", "start_server.py"],
                     creationflags=subprocess.CREATE_NEW_CONSOLE)


def start_counter():
    subprocess.Popen(["python", "start_counter.py"],
                     creationflags=subprocess.CREATE_NEW_CONSOLE)


def main():
    print("Starting API...")
    start_api()
    print("Starting Counter...")
    start_counter()



if __name__ == '__main__':
    main()
    print("Done.")
