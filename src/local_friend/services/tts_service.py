import threading
import pyttsx3


class TTSService:
    def __init__(self) -> None:
        self._enabled = False
        self._lock = threading.Lock()
        self._engine = pyttsx3.init()
        self._engine.setProperty("rate", 160)
        self._engine.setProperty("volume", 1.0)

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled

    def is_enabled(self) -> bool:
        return self._enabled

    def speak(self, text: str) -> None:
        """Läser upp text i en separat tråd så UI inte fryser."""
        if not self._enabled:
            return

        def _run():
            with self._lock:
                self._engine.say(text)
                self._engine.runAndWait()

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()