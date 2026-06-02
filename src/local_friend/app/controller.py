from PyQt6.QtCore import QObject
from local_friend.ui.overlay import PetOverlay
from local_friend.workers.assistant_worker import AssistantWorker


class AppController(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.overlay = PetOverlay()
        self.worker = AssistantWorker()
        self._connect_signals()

    def _connect_signals(self) -> None:
        # Worker → UI
        self.worker.status_update.connect(self.overlay.update_status)
        self.worker.new_commentary.connect(self.overlay.update_speech)

        # Hide/show för capture
        self.worker.request_hide.connect(self.overlay.hide_for_capture)
        self.worker.request_show.connect(self.overlay.show)
        self.overlay.overlay_hidden.connect(self.worker.on_overlay_hidden)
        
        # Avatar → persona-koppling
        self.overlay.avatar_changed.connect(
            self.worker.commentary_service.set_avatar
        )

    def start(self) -> None:
        self.overlay.show()
        self.worker.start()