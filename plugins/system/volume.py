import time
from core.plugin_base import PluginBase

try:
    import pycaw
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
except ImportError:
    pycaw = None


class VolumePlugin(PluginBase):
    name = "volume_control"
    intents = ["VOLUME_CONTROL"]

    permission = "system.write"
    requires_confirmation = False

    def _get_volume_interface(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        return cast(interface, POINTER(IAudioEndpointVolume))

    def _get_current_volume(self, volume):
        # Returns volume in percentage (0–100)
        return int(volume.GetMasterVolumeLevelScalar() * 100)

    def _set_absolute_volume(self, volume, target):
        target = max(0, min(100, target))
        volume.SetMasterVolumeLevelScalar(target / 100.0, None)
        return f"Volume set to {target}%."

    def _step_volume(self, volume, step):
        current = self._get_current_volume(volume)
        target = max(0, min(100, current + step))
        volume.SetMasterVolumeLevelScalar(target / 100.0, None)
        return f"Volume changed to {target}%."

    def execute(self, context):
        if not pycaw:
            return {
                "success": False,
                "response": "Volume control is not supported on this system.",
                "data": {}
            }

        entities = context.get("entities", {})
        action = entities.get("action")
        level = entities.get("level")

        volume = self._get_volume_interface()

        # 🔇 Mute / Unmute
        if action == "mute":
            volume.SetMute(1, None)
            return {"success": True, "response": "Volume muted.", "data": {}}

        if action == "unmute":
            volume.SetMute(0, None)
            return {"success": True, "response": "Volume unmuted.", "data": {}}

        # 🎯 Absolute set (Alexa-style)
        if action == "set" and isinstance(level, int):
            return {
                "success": True,
                "response": self._set_absolute_volume(volume, level),
                "data": {"level": level}
            }

        # 🔼 Relative increase / decrease
        if action == "increase":
            return {
                "success": True,
                "response": self._step_volume(volume, 5),
                "data": {}
            }

        if action == "decrease":
            return {
                "success": True,
                "response": self._step_volume(volume, -5),
                "data": {}
            }

        return {
            "success": False,
            "response": "I didn’t understand the volume command.",
            "data": {}
        }
