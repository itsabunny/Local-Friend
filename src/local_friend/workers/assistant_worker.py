import time
from PyQt6.QtCore import QThread, pyqtSignal

from local_friend.config import (
    CAPTURE_INTERVAL_SECONDS,
    COUNTDOWN_UPDATE_MS,
)
from local_friend.capture.screen_capture import capture_primary_screen
from local_friend.services.commentary_service import (
    prepare_image_for_model,
    CommentaryService,
)


class AssistantWorker(QThread):
    status_update = pyqtSignal(str)
    new_commentary = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.commentary_service = CommentaryService()

    def run(self) -> None:
        last_run_time = time.time() - CAPTURE_INTERVAL_SECONDS

        while True:
            current_time = time.time()

            if current_time - last_run_time >= CAPTURE_INTERVAL_SECONDS:
                self.status_update.emit("🤔 Thinking...")

                image = capture_primary_screen()
                image = prepare_image_for_model(image)

                commentary = self.commentary_service.get_new_commentary(image)

                # TILLFÄLLIG DEBUG - ta bort senare
                print(f"[DEBUG] commentary = {repr(commentary)}")

                if commentary:
                    self.new_commentary.emit(commentary)
                    self.status_update.emit("✨ Done!")
                else:
                    self.status_update.emit("💤 Nothing new...")

                last_run_time = time.time()
            else:
                remaining = int(CAPTURE_INTERVAL_SECONDS - (current_time - last_run_time))
                self.status_update.emit(f"Next capture in {remaining}s")

            self.msleep(COUNTDOWN_UPDATE_MS)