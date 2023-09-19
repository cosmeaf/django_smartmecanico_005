# utils/machine/get_data_machine.py

import platform
import os

def get_machine_info():
    system_info = {
        "os_name": platform.system(),
        "os_version": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }
    
    if system_info["os_name"].lower() == "linux":
        distro_name, distro_version, _ = platform.linux_distribution()
        system_info["linux_distro"] = distro_name
        system_info["linux_distro_version"] = distro_version
    elif system_info["os_name"].lower() == "darwin":
        system_info["os_name"] = "MacOS"
        
    return system_info

# Testando
if __name__ == "__main__":
    print(get_machine_info())
