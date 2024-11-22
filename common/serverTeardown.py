import platform
import os


def stop_server(server_name):
    current_os = platform.system()
    if current_os == "Windows":
        os.system("taskkill /IM {}.exe /F".format(server_name))
    elif current_os == "Linux":
        os.system("pkill -f {}.py".format(server_name))
    else:
        print("Unknown")

