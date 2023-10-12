import platform
import os
import distro
from user_agents import parse

def get_machine_info():
    system_info = {
        "os_name": platform.system(),
        "os_version": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }
    
    if system_info["os_name"].lower() == "linux":
        distro_name = distro.name()
        distro_version = distro.version()
        system_info["linux_distro"] = distro_name
        system_info["linux_distro_version"] = distro_version
    elif system_info["os_name"].lower() == "darwin":
        system_info["os_name"] = "MacOS"
        
    return system_info



def get_client_info(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)
    
    client_info = {
        "os_name": user_agent.os.family,
        "os_version": user_agent.os.version_string,
        "browser": user_agent.browser.family,
        "device": user_agent.device.family,
        "device_type": "Mobile" if user_agent.is_mobile else "Desktop"
    }

    return client_info



if __name__ == "__main__":
    machine_info = get_machine_info()
    print("Machine Info:", machine_info)
