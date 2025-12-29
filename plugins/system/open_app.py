# plugins/system/open_app.py

import subprocess
import json
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
            # 1️⃣ Query Windows Start Menu apps
            ps_command = (
                "Get-StartApps | "
                f"Where-Object {{$_.Name -match '{app}'}} | "
                "Select-Object -First 1 -Property AppID | "
                "ConvertTo-Json"
            )

            result = subprocess.check_output(
                ["powershell", "-NoProfile", "-Command", ps_command],
                text=True
            ).strip()

            if not result:
                raise RuntimeError("App not found in Start Menu")

            app_id = json.loads(result)["AppID"]

            # 2️⃣ Launch via AppsFolder
            subprocess.Popen(
                ["explorer.exe", f"shell:AppsFolder\\{app_id}"],
                shell=False
            )

            return {
                "success": True,
                "response": f"Opening {app}.",
                "data": {"app_id": app_id}
            }

        except Exception as e:
            return {
                "success": False,
                "response": f"Couldn't find {app} on this system.",
                "data": {"error": str(e)}
            }
