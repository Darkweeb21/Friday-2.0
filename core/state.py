from core.confirmation import ConfirmationManager
import uuid

#  Confirmation manager
confirmation_manager = ConfirmationManager()

# Unique session per run
SESSION_ID = str(uuid.uuid4())

# RAM chat memory (short-term)
CHAT_MEMORY_LIMIT = 6
chat_history = []  # [{"role": "user"/"assistant", "content": str}]

# Action / context memory
last_intent = None
last_entities = None
last_action = None

# 🎙Voice state
mic_enabled = False
speech_enabled = True
mic_temporarily_disabled = False

# Speech state
is_speaking = False
