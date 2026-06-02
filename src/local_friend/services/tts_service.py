import queue
import threading


class TTSService:
    def __init__(self) -> None:
        self._enabled = False
        self._queue: queue.Queue = queue.Queue()
        self._worker = threading.Thread(target=self._run, daemon=True)
        self._worker.start()

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled

    def is_enabled(self) -> bool:
        return self._enabled

    def speak(self, text: str) -> None:
        if not self._enabled or not text:
            return
        self._queue.put(text)

    def _run(self) -> None:
        while True:
            text = self._queue.get()
            try:
                self._speak_fresh(text)
            except Exception as e:
                print(f"[TTS] Fel: {e}")
            finally:
                self._queue.task_done()

    def _speak_fresh(self, text: str) -> None:
        """Skapar en ny motor för varje meddelande – kringgår Windows-buggen."""
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()