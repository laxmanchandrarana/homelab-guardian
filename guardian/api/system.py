import psutil
import shutil
import platform
import socket


def info():
    return {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "cpu_percent": psutil.cpu_percent(),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": shutil.disk_usage("/")._asdict(),
        "boot_time": psutil.boot_time()
    }
