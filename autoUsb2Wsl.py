import subprocess
import re
import time

import psutil


def execute_cmd(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr


def get_usb_devices():
    output = execute_cmd("usbipd list|findstr Shared")
    usb_ids = re.compile(r"\d+-\d+", re.IGNORECASE).findall(output)
    if len(usb_ids) > 0:
        for usb_id in usb_ids:
            execute_cmd(f"usbipd attach --wsl --busid {usb_id}")


def check_process_exists(process_name):
    count = 0
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            if proc.info["name"] == process_name:
                count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    if count > 2:
        return True
    return False


# Set the sleep time in seconds
sleep_time = 5
proc_name = "autoUsb2Wsl.exe"
if __name__ == "__main__":
    # Check if the process is already running
    if check_process_exists(proc_name):
        # If the process is already running, exit the script
        exit()
    try:
        # Start the main loop
        while True:
            get_usb_devices()
            time.sleep(sleep_time)
    except Exception as e:
        print(e)
        input("Press any key to exit...")
