import platform
import psutil


def device_specs() -> str:
    cpu = platform.processor()
    ram = round(psutil.virtual_memory().total / (1024 ** 3), 1)
    os_name = platform.system()
    os_version = platform.version()
    architecture = platform.machine()

    return (
        f"Device specifications:\n"
        f"CPU: {cpu}\n"
        f"RAM: {ram} GB\n"
        f"OS: {os_name} ({os_version})\n"
        f"Architecture: {architecture}"
    )
