# plugins/system/open_app.py

import subprocess
from core.plugin_base import PluginBase


class OpenAppPlugin(PluginBase):
    name = "open_app"
    intents = ["OPEN_APP"]

    permission = "system.write"
    requires_confirmation = False

    def execute(self, context):
        app = context.get("entities", {}).get("app")

        if not app:
            return {
                "success": False,
                "response": "Which application should I open?",
                "data": {}
            }

        try:
            # 🔑 This is equivalent to Win + R → typing the app name
            subprocess.Popen(app, shell=True)

            return {
                "success": True,
                "response": f"Opening {app}.",
                "data": {}
            }

        except Exception as e:
            return {
                "success": False,
                "response": f"Failed to open {app}.",
                "data": {"error": str(e)}
            }
