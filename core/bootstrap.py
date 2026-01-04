"""
Application bootstrap module.

Responsibilities:
- Force-load all plugins so they self-register
- Ensure PLUGIN_REGISTRY is populated
- Shared by ALL entry points (CLI, API, future services)
"""

# ================= SYSTEM PLUGINS =================
import plugins.system.open_app
import plugins.system.close_app
import plugins.system.volume
import plugins.system.screenshot
import plugins.system.system_status
import plugins.system.power
import plugins.system.voice_toggle

# ================= CHAT & PRODUCTIVITY PLUGINS =================
import plugins.chat.general_chat
import plugins.productivity.reminders
import plugins.productivity.notes
import plugins.productivity.alarms
import plugins.Memory.memory_recall
