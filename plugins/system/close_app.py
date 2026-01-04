# plugins/system/close_app.py

import subprocess
from core.plugin_base import PluginBase
from core import state


class CloseAppPlugin(PluginBase):
    name = "close_app"
    intents = ["CLOSE_APP"]

    permission = "system.write"
    requires_confirmation = False

    def execute(self, context):
        # 1️⃣ Try explicit entity first
        app = context.get("entities", {}).get("app")

        # 2️⃣ Fallback to short-term memory (contextual command)
        if not app and state.last_entities:
            app = state.last_entities.get("app")

        if not app:
            return {
                "success": False,
                "response": "Which application should I close?",
                "data": {}
            }

        try:
            result = subprocess.run(
                f'taskkill /IM "{app}.exe" /F',
                shell=True,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "response": f"Closed {app}.",
                    "data": {"app": app}
                }

            return {
                "success": False,
                "response": f"{app} is not running.",
                "data": {"app": app}
            }

        except Exception as e:
            return {
                "success": False,
                "response": f"Failed to close {app}.",
                "data": {"error": str(e)}
            }
