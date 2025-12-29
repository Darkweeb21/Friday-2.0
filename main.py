# main.py
from core.state import confirmation_manager
from models.intent_model import IntentModel
from core.router import route
# 🔌 Force plugin imports (REQUIRED for registration)
import plugins.system.open_app
import plugins.system.close_app
import plugins.system.volume
import plugins.system.screenshot
import plugins.system.system_status
import plugins.system.power
import plugins.chat.general_chat
import plugins.productivity.reminders
import plugins.productivity.notes
import plugins.productivity.alarms
import plugins.Memory.memory_recall
from core.confirmation import ConfirmationManager

def main():
    print("FRIDAY online. Debug mode enabled.")

    intent_model = IntentModel()

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        # 🔴 CONFIRMATION INTERCEPT (CRITICAL)
        if confirmation_manager.has_pending():
            normalized = user_input.lower()

            if normalized in ("yes", "y", "confirm", "ok", "sure"):
                result = confirmation_manager.confirm()
                print("FRIDAY:", "Done.")
                continue

            if normalized in ("no", "n", "cancel", "stop"):
                result = confirmation_manager.cancel()
                print("FRIDAY:", result)
                continue

            print("FRIDAY: Please say yes or no.")
            continue

        # 🟢 Normal flow
        intent_data = intent_model.classify(user_input)
        response = route(intent_data, user_input)

        if response == "EXIT":
            print("FRIDAY: Shutting down.")
            break

        print("FRIDAY:", response)



if __name__ == "__main__":
    main()
