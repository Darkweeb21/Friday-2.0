# core/intents.py

INTENTS = {
    # System
    "OPEN_APP": "Open a system application",
    "CLOSE_APP": "Close a running application",
    "VOLUME_CONTROL": "Control system volume",
    "SYSTEM_STATUS": "Get system status",
    "SCREENSHOT": "Take a screenshot",
    "POWER_CONTROL": "Lock, shutdown, or restart system",

    # Productivity — Reminders
    "SET_REMINDER": "Create a reminder",
    "SHOW_REMINDERS": "List reminders",
    "CLEAR_REMINDERS": "Delete reminders",

    # Productivity — Notes
    "TAKE_NOTE": "Save a note",
    "SHOW_NOTES": "List notes",
    "CLEAR_NOTES": "Delete notes",

    # Productivity — Alarms
    "SET_ALARM": "Create an alarm",
    "SHOW_ALARMS": "List alarms",
    "CLEAR_ALARMS": "Delete alarms",



    # Chat / Control
    "GENERAL_CHAT": "General conversation",
    "HELP": "Show help",
    "EXIT": "Exit assistant",
    "CONFIRM": "Confirm action",
    "CANCEL": "Cancel action",
    "REPEAT": "Repeat last action",
    "MEMORY_RECALL": "Recall memory",

    "UNKNOWN": "Unknown intent",
}
