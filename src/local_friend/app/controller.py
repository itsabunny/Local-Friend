from PyQt6.QtCore import QObject
from local_friend.ui.overlay import PetOverlay
from local_friend.workers.assistant_worker import AssistantWorker
from local_friend.services.tts_service import TTSService


class AppController(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.overlay = PetOverlay()
        self.worker = AssistantWorker()
        self.tts = TTSService()
        self._connect_signals()

    def _connect_signals(self) -> None:
        # Worker → UI
        self.worker.status_update.connect(self.overlay.update_status)
        self.worker.new_commentary.connect(self.overlay.update_speech)

        # Worker → TTS
        self.worker.new_commentary.connect(self._on_new_commentary)

        # Hide/show for capture
        self.worker.request_hide.connect(self.overlay.hide_for_capture)
        self.worker.request_show.connect(self.overlay.show)
        self.overlay.overlay_hidden.connect(self.worker.on_overlay_hidden)

        # Avatar → persona connection
        self.overlay.avatar_changed.connect(
            self.worker.commentary_service.set_avatar
        )

        # TTS toggle
        self.overlay.tts_toggled.connect(self.tts.set_enabled)

        # Interval and model
        self.overlay.interval_changed.connect(self.worker.set_interval)
        self.overlay.model_changed.connect(self.worker.set_model)

        # NEW: Chat mode toggle → pause/resume worker
        self.overlay.chat_mode_toggled.connect(self.worker.set_paused)

        # NEW: Question from the user → worker handles it
        self.overlay.question_asked.connect(self.worker.ask_question)

    def _on_new_commentary(self, text: str) -> None:
        self.tts.speak(text)

    def start(self) -> None:
        self.overlay.show()
        self.worker.start()