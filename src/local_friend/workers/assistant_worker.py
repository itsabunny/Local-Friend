import time
import threading
from PyQt6.QtCore import QThread, pyqtSignal

from local_friend.config import (
    CAPTURE_INTERVAL_SECONDS,
    COUNTDOWN_UPDATE_MS,
    CAPTURE_HIDE_DELAY_MS,
)
from local_friend.capture.screen_capture import capture_primary_screen
from local_friend.services.commentary_service import (
    prepare_image_for_model,
    CommentaryService,
)


class AssistantWorker(QThread):
    status_update = pyqtSignal(str)
    new_commentary = pyqtSignal(str)
    request_hide = pyqtSignal()   # be overlay gömma sig
    request_show = pyqtSignal()   # be overlay visa sig

    def __init__(self) -> None:
        super().__init__()
        self.commentary_service = CommentaryService()
        self._hidden_event = threading.Event()  # synkronisering
        self._interval_sec = CAPTURE_INTERVAL_SECONDS  # NY: dynamiskt intervall

    def on_overlay_hidden(self) -> None:
        """Anropas av overlay (via signal) när den faktiskt är gömd."""
        self._hidden_event.set()

    def set_interval(self, seconds: int) -> None:
        """Ändrar hur ofta skärmdumpar tas."""
        self._interval_sec = seconds
        self.status_update.emit(f"⏱️ Intervall: {seconds}s")

    def set_model(self, model_name: str) -> None:
        """Byter AI-modell som används för bildanalys."""
        self.commentary_service.ai_client.model = model_name
        self.status_update.emit(f"🧠 Modell: {model_name}")

    def run(self) -> None:
        last_run_time = time.time() - self._interval_sec

        while True:
            current_time = time.time()

            if current_time - last_run_time >= self._interval_sec:
                self.status_update.emit("📸 Capturing...")

                # 1. Be overlay gömma sig
                self._hidden_event.clear()
                self.request_hide.emit()

                # 2. Vänta tills overlay bekräftar att den är gömd (max 1s)
                self._hidden_event.wait(timeout=1.0)

                # 3. Ta skärmdump (overlay är nu gömd)
                image = capture_primary_screen()

                # 4. Be overlay visa sig igen
                self.request_show.emit()

                # 5. Bearbeta och skicka till AI
                self.status_update.emit("🤔 Thinking...")
                image = prepare_image_for_model(image)
                commentary = self.commentary_service.get_new_commentary(image)

                if commentary:
                    self.new_commentary.emit(commentary)
                    self.status_update.emit("✨ Done!")
                else:
                    self.status_update.emit("💤 Nothing new...")

                last_run_time = time.time()
            else:
                remaining = int(self._interval_sec - (current_time - last_run_time))
                self.status_update.emit(f"Next capture in {remaining}s")

            self.msleep(COUNTDOWN_UPDATE_MS)