# plugins/system/system_status.py

import psutil
import datetime
from core.plugin_base import PluginBase

# Optional GPU support (safe import)
try:
    import GPUtil
except ImportError:
    GPUtil = None


class SystemStatusPlugin(PluginBase):
    name = "system_status"
    intents = ["SYSTEM_STATUS"]

    permission = "system.read"
    requires_confirmation = False

    def execute(self, context):
        query = context.get("entities", {}).get("type")

        # CPU
        if query == "cpu":
            cpu = psutil.cpu_percent(interval=1)
            return {
                "success": True,
                "response": f"CPU usage is {cpu}%.",
                "data": {}
            }

        # Memory
        if query == "memory":
            mem = psutil.virtual_memory()
            return {
                "success": True,
                "response": f"Memory usage is {mem.percent}%.",
                "data": {}
            }

        # Battery
        if query == "battery":
            batt = psutil.sensors_battery()
            if not batt:
                return {
                    "success": False,
                    "response": "Battery information is not available.",
                    "data": {}
                }
            return {
                "success": True,
                "response": f"Battery is at {batt.percent}%.",
                "data": {}
            }

        # Time
        if query == "time":
            now = datetime.datetime.now().strftime("%I:%M %p")
            return {
                "success": True,
                "response": f"The time is {now}.",
                "data": {}
            }

        # GPU (optional)
        if query == "gpu":
            if not GPUtil:
                return {
                    "success": False,
                    "response": "GPU information is not available on this system.",
                    "data": {}
                }

            gpus = GPUtil.getGPUs()
            if not gpus:
                return {
                    "success": False,
                    "response": "GPU information is not available.",
                    "data": {}
                }

            usage = gpus[0].load * 100
            return {
                "success": True,
                "response": f"GPU usage is {usage:.0f}%.",
                "data": {}
            }

        # Fallback
        return {
            "success": True,
            "response": "CPU, memory, battery, time, or GPU?",
            "data": {}
        }
