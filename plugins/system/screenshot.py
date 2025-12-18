import os
from datetime import datetime
import pyautogui


def take_screenshot() -> str:
    try:
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        path = os.path.join(screenshots_dir, filename)

        image = pyautogui.screenshot()
        image.save(path)

        return f"Screenshot taken and saved."
    except Exception:
        return "Failed to take screenshot."
