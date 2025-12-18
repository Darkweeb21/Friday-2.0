# plugins/system/volume.py

import ctypes
import time

# Windows virtual key codes
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002


def _press_key(vk_code, times=1, delay=0.05):
    for _ in range(times):
        ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY, 0)
        ctypes.windll.user32.keybd_event(
            vk_code, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0
        )
        time.sleep(delay)


def increase_volume():
    _press_key(VK_VOLUME_UP, times=3)
    return "Volume increased."


def decrease_volume():
    _press_key(VK_VOLUME_DOWN, times=3)
    return "Volume decreased."


def mute_volume():
    _press_key(VK_VOLUME_MUTE, times=1)
    return "Volume muted."


def unmute_volume():
    _press_key(VK_VOLUME_MUTE, times=1)
    return "Volume unmuted."


def set_volume(level: int):
    """
    Deterministic volume setting using media keys.
    First forces volume to 0, then raises to target level.
    """
    level = max(0, min(level, 100))

    # Step 1: Force volume to minimum
    _press_key(VK_VOLUME_DOWN, times=50)

    # Step 2: Raise volume to target
    steps = int(level / 2)  # ~2% per key press (empirical)
    _press_key(VK_VOLUME_UP, times=steps)

    return f"Volume set approximately to {level}%."

