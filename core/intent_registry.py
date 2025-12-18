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



INTENT_REGISTRY = {
    "OPEN_APP": open_app_handler,
    "CLOSE_APP": close_app_handler,
    "VOLUME_CONTROL": volume_handler,
    "SCREENSHOT": screenshot_handler,
    "POWER_CONTROL": power_handler,
    "GENERAL_CHAT": lambda e: "Chat handling will be added next.",
    "EXIT": lambda e: "EXIT",
}
