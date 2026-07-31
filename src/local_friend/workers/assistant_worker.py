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
    request_hide = pyqtSignal()
    request_show = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.commentary_service = CommentaryService()
        self._hidden_event = threading.Event()
        self._interval_sec = CAPTURE_INTERVAL_SECONDS
        self._paused = False          # NEW: is auto mode paused?
        self._question_event = threading.Event()   # NEW: signal that a question is waiting
        self._pending_question: str | None = None  # NEW: the question that is waiting

    def on_overlay_hidden(self) -> None:
        """Called by the overlay (via signal) when it is actually hidden."""
        self._hidden_event.set()

    def set_interval(self, seconds: int) -> None:
        """Changes how often screenshots are taken."""
        self._interval_sec = seconds
        self.status_update.emit(f"⏱️ Intervall: {seconds}s")

    def set_model(self, model_name: str) -> None:
        """Switches the AI model used for image analysis."""
        self.commentary_service.ai_client.set_model(model_name)
        self.status_update.emit(f"🧠 Modell: {model_name}")

    def set_paused(self, paused: bool) -> None:
        """Pauses or resumes auto mode."""
        self._paused = paused
        if paused:
            self.status_update.emit("⏸️ Auto-läge avstängt")
        else:
            self.status_update.emit("▶️ Auto-läge aktivt")

    def ask_question(self, question: str) -> None:
        """
        Called from the UI thread when the user asks a question.
        Stores the question and signals that the worker thread should handle it.
        """
        self._pending_question = question
        self._question_event.set()

    def _handle_question(self, question: str) -> None:
        """Takes a screenshot and answers the user's question."""
        self.status_update.emit("🤔 Thinking...")

        # Hide overlay, take screenshot, show overlay again
        self._hidden_event.clear()
        self.request_hide.emit()
        self._hidden_event.wait(timeout=1.0)

        image = capture_primary_screen()
        self.request_show.emit()

        # Process and send to AI with the question
        image = prepare_image_for_model(image)
        answer = self.commentary_service.get_answer(image, question)

        self.new_commentary.emit(answer)
        self.status_update.emit("✨ Done!")

    def run(self) -> None:
        last_run_time = time.time() - self._interval_sec

        while True:
            # Check if a question is waiting – always handled, regardless of mode
            if self._question_event.is_set():
                self._question_event.clear()
                question = self._pending_question
                self._pending_question = None
                if question:
                    self._handle_question(question)
                last_run_time = time.time()  # reset timer after question
                self.msleep(COUNTDOWN_UPDATE_MS)
                continue

            # Auto mode
            if self._paused:
                self.status_update.emit("⏸️ Chat-läge aktivt")
                self.msleep(COUNTDOWN_UPDATE_MS)
                continue

            current_time = time.time()

            if current_time - last_run_time >= self._interval_sec:
                self.status_update.emit("📸 Capturing...")

                self._hidden_event.clear()
                self.request_hide.emit()
                self._hidden_event.wait(timeout=1.0)

                image = capture_primary_screen()
                self.request_show.emit()

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