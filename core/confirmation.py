class ConfirmationManager:
    def __init__(self):
        self.pending_action = None

    def set(self, action_callable, message: str):
        self.pending_action = action_callable
        return message

    def confirm(self):
        if self.pending_action:
            action = self.pending_action
            self.pending_action = None
            return action()
        return "Nothing to confirm."

    def cancel(self):
        if self.pending_action:
            self.pending_action = None
            return "Action cancelled."
        return "Nothing to cancel."

    def has_pending(self):
        return self.pending_action is not None
