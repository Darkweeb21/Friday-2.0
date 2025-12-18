# plugins/system/open_app.py

import subprocess
import os
import shutil
from typing import Optional, List


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


SEARCH_DIRS = [
    os.environ.get("ProgramFiles", ""),
    os.environ.get("ProgramFiles(x86)", ""),
    os.environ.get("LOCALAPPDATA", ""),
]


def find_executable_by_name(exe_name: str) -> Optional[str]:
    # Check PATH
    path = shutil.which(exe_name)
    if path:
        return path

    # Search common install locations
    for base in SEARCH_DIRS:
        if not base:
            continue
        for root, _, files in os.walk(base):
            for f in files:
                if f.lower() == exe_name.lower():
                    return os.path.join(root, f)

    return None


def fuzzy_find_app(app_name: str) -> List[str]:
    """
    Find executables loosely matching the app name.
    """
    matches = []
    app_name = app_name.lower()

    for base in SEARCH_DIRS:
        if not base:
            continue
        for root, _, files in os.walk(base):
            for f in files:
                if app_name in f.lower() and f.lower().endswith(".exe"):
                    matches.append(os.path.join(root, f))

    return matches


def open_app(app_name: str) -> str:
    if not app_name:
        return "No application name provided."

    key = app_name.lower()

    # 1️⃣ Known alias
    exe = KNOWN_ALIASES.get(key)
    if exe:
        exe_path = find_executable_by_name(exe)
        if exe_path:
            subprocess.Popen([exe_path], shell=False)
            return f"Opening {app_name}."
        return f"{app_name} is not installed."

    # 2️⃣ Fuzzy search
    matches = fuzzy_find_app(key)

    if len(matches) == 1:
        subprocess.Popen([matches[0]], shell=False)
        return f"Opening {app_name}."

    if len(matches) > 1:
        return (
            f"I found multiple applications matching '{app_name}'. "
            "Please be more specific."
        )

    return f"I couldn't find an installed application named '{app_name}'."
