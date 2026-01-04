from output.speech import speak

def respond(text: str):
    print(f"FRIDAY: {text}")
    speak(text)
