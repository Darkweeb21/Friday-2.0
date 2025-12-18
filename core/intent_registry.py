def open_app_handler(entities):
    from plugins.system.open_app import open_app
    return open_app(entities.get("app"))


def close_app_handler(entities):
    from plugins.system.close_app import close_app
    return close_app(entities.get("app"))


def screenshot_handler(entities):
    from plugins.system.screenshot import take_screenshot
    return take_screenshot()


def volume_handler(entities):
    from plugins.system.volume import (
        increase_volume,
        decrease_volume,
        set_volume,
        mute_volume,
        unmute_volume,
    )

    action = entities.get("action")
    level = entities.get("level")

    if action == "increase":
        return increase_volume()
    if action == "decrease":
        return decrease_volume()
    if action == "mute":
        return mute_volume()
    if action == "unmute":
        return unmute_volume()
    if action == "set" and isinstance(level, int):
        return set_volume(level)

    return "I didn't understand the volume command."


def power_handler(entities):
    from plugins.system.power import (
        lock_system,
        shutdown_system,
        restart_system
    )
    from core.state import confirmation_manager

    action = entities.get("action")

    if action == "lock":
        return confirmation_manager.set(
            lock_system,
            "Are you sure you want to lock the system? Say confirm or cancel."
        )

    if action == "shutdown":
        return confirmation_manager.set(
            shutdown_system,
            "Are you sure you want to shut down? Say confirm or cancel."
        )

    if action == "restart":
        return confirmation_manager.set(
            restart_system,
            "Are you sure you want to restart? Say confirm or cancel."
        )

    return "I didn't understand the power command."

def system_status_handler(entities):
    from plugins.system.status import (
        cpu_usage,
        memory_usage,
        battery_status,
        current_time
    )

    query = entities.get("type")

    if query == "cpu":
        return cpu_usage()
    if query == "memory":
        return memory_usage()
    if query == "battery":
        return battery_status()
    if query == "time":
        return current_time()

    return "I didn't understand the system status request."
def system_status_handler(entities):
    from plugins.system.status import (
        cpu_usage,
        memory_usage,
        battery_status,
        current_time,
        gpu_usage
    )
    from plugins.system.specs import device_specs

    query = entities.get("type")

    if query == "cpu":
        return cpu_usage()
    if query == "memory":
        return memory_usage()
    if query == "battery":
        return battery_status()
    if query == "time":
        return current_time()
    if query == "gpu":
        return gpu_usage()

    # ✅ FALLBACK: if no type → return full device specs
    return device_specs()
def general_chat_handler(entities):
    from plugins.chat.general_chat import chat_response
    return chat_response(entities.get("text", ""))


INTENT_REGISTRY = {
    "OPEN_APP": open_app_handler,
    "CLOSE_APP": close_app_handler,
    "VOLUME_CONTROL": volume_handler,
    "SCREENSHOT": screenshot_handler,
    "POWER_CONTROL": power_handler,
    "GENERAL_CHAT": lambda e: "Chat handling will be added next.",
    "EXIT": lambda e: "EXIT",
    "SYSTEM_STATUS": system_status_handler,
    "GENERAL_CHAT": general_chat_handler,
}
