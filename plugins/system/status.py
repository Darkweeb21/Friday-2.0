import psutil
from datetime import datetime
import subprocess

def cpu_usage() -> str:
    cpu = psutil.cpu_percent(interval=1)
    return f"CPU usage is {cpu}%."


def memory_usage() -> str:
    mem = psutil.virtual_memory()
    return f"Memory usage is {mem.percent}%."


def battery_status() -> str:
    battery = psutil.sensors_battery()
    if battery is None:
        return "Battery information is not available."
    percent = battery.percent
    plugged = "plugged in" if battery.power_plugged else "on battery"
    return f"Battery is at {percent}% and {plugged}."


def current_time() -> str:
    now = datetime.now().strftime("%I:%M %p")
    return f"The time is {now}."



def gpu_usage() -> str:
    try:
        result = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=utilization.gpu",
                "--format=csv,noheader,nounits",
            ],
            stderr=subprocess.DEVNULL
        )
        usage = result.decode().strip()
        return f"GPU usage is {usage}%."
    except Exception:
        return "GPU usage information is not available."
