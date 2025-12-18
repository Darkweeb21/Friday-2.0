# main.py

from models.intent_model import IntentModel
from core.router import route


def main():
    print("FRIDAY online. Debug mode enabled.")

    intent_model = IntentModel()

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        intent_data = intent_model.classify(user_input)
        response = route(intent_data)

        if response == "EXIT":
            print("FRIDAY: Shutting down.")
            break

        print("FRIDAY:", response)


if __name__ == "__main__":
    main()
