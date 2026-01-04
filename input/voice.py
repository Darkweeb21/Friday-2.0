import os

from core.paths import FFMPEG_DIR
from core import state

# Add FFmpeg to PATH (centralized)
os.environ["PATH"] += os.pathsep + str(FFMPEG_DIR)

import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav
import os


class VoiceInput:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)
        self.sample_rate = 16000
        self.duration = 5  # seconds

    def listen(self):
        if not state.mic_enabled or state.mic_temporarily_disabled:
            return None

        print("🎙️ Listening...")

        recording = sd.rec(
            int(self.duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.int16
        )
        sd.wait()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            wav.write(f.name, self.sample_rate, recording)
            audio_path = f.name

        try:
            result = self.model.transcribe(audio_path)
            text = result.get("text", "").strip()
            return text if text else None
        finally:
            os.remove(audio_path)
