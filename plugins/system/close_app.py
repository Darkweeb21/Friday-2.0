# plugins/system/close_app.py

import subprocess

KNOWN_ALIASES = {
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "edge": "msedge.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "vscode": "code.exe",
    "visual studio code": "code.exe",
    "spotify": "spotify.exe",
}


def close_app(app_name: str) -> str:
    if not app_name:
        return "No application name provided."

    key = app_name.lower()
    exe = KNOWN_ALIASES.get(key)

    if not exe:
        return f"I don't know how to close {app_name}."

    try:
        result = subprocess.run(
            ["taskkill", "/IM", exe, "/F"],
            capture_output=True,
            text=True,
            shell=True
        )

        if result.returncode == 0:
            return f"Closed {app_name}."
        else:
            return f"{app_name} is not running."

    except Exception:
        return f"Failed to close {app_name}."
