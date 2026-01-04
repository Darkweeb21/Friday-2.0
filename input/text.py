class TextInput:
    def listen(self):
        try:
            text = input("You (text): ").strip()
            return text if text else None
        except EOFError:
            return None
