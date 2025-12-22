# main.py

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



def main():
    print("FRIDAY online. Debug mode enabled.")

    intent_model = IntentModel()

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        intent_data = intent_model.classify(user_input)
        response = route(intent_data, user_input)


        if response == "EXIT":
            print("FRIDAY: Shutting down.")
            break

        print("FRIDAY:", response)


if __name__ == "__main__":
    main()
