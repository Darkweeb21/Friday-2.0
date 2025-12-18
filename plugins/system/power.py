import os


def lock_system() -> str:
    try:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "System locked."
    except Exception:
        return "Failed to lock the system."


def shutdown_system() -> str:
    try:
        os.system("shutdown /s /t 5")
        return "System will shut down in 5 seconds."
    except Exception:
        return "Failed to shut down the system."


def restart_system() -> str:
    try:
        os.system("shutdown /r /t 5")
        return "System will restart in 5 seconds."
    except Exception:
        return "Failed to restart the system."
