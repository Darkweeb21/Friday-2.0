# plugins/system/screenshot.py

import datetime
from pathlib import Path
import pyautogui
from core.plugin_base import PluginBase


class ScreenshotPlugin(PluginBase):
    name = "screenshot"
    intents = ["SCREENSHOT"]

    permission = "system.read"
    requires_confirmation = False

    def execute(self, context):
        try:
            base_dir = Path.home() / "Pictures" / "FRIDAY"
            base_dir.mkdir(parents=True, exist_ok=True)

            filename = datetime.datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.png")
            path = base_dir / filename

            screenshot = pyautogui.screenshot()
            screenshot.save(path)

            return {
                "success": True,
                "response": "Screenshot taken.",
                "data": {"path": str(path)}
            }

        except Exception as e:
            return {
                "success": False,
                "response": "Failed to take screenshot.",
                "data": {"error": str(e)}
            }
