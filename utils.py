import os
from sys import platform

import consts


def get_os():
    if platform.lower() == "linux":
        # Check if it's Ubuntu
        if os.path.isfile("/etc/os-release"):
            with open("/etc/os-release") as f:
                os_info = f.read()
                if "Ubuntu" in os_info:
                    return consts.OS_UBUNTU
        return "Linux (Not Ubuntu)"
    elif platform.lower() == "darwin":
        return consts.OS_MAC
    else:
        return "Unknown OS"