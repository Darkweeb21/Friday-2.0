# plugins/system/power_control.py
# used for system piwer suc h as shutdown restart etc
import os
from core.plugin_base import PluginBase
from core.state import confirmation_manager


class PowerControlPlugin(PluginBase):
    name = "power_control"
    intents = ["POWER_CONTROL"]

    permission = "system.write"
    requires_confirmation = True

    def execute(self, context):
        action = context.get("entities", {}).get("action")

        if action == "lock":
            return confirmation_manager.set(
                lambda: os.system("rundll32.exe user32.dll,LockWorkStation"),
                "Are you sure you want to lock the system?"
            )

        if action == "shutdown":
            return confirmation_manager.set(
                lambda: os.system("shutdown /s /t 5"),
                "Are you sure you want to shut down the system?"
            )

        if action == "restart":
            return confirmation_manager.set(
                lambda: os.system("shutdown /r /t 5"),
                "Are you sure you want to restart the system?"
            )

        return {
            "success": False,
            "response": "Lock, shutdown, or restart?",
            "data": {}
        }
