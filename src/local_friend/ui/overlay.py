from PyQt6.QtCore import Qt, QRect, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QApplication,
    QMenu,
    QLineEdit,
    QPushButton,
)

from local_friend.ui.widgets import SpeechBubble, StatusLabel, AvatarWidget, AVATARS
from local_friend.ai.ollama_models import get_installed_ollama_models
from local_friend.config import (
    CAPTURE_HIDE_DELAY_MS,
    DEFAULT_AVATAR_TEXT,
    DEFAULT_BUBBLE_TEXT,
    DEFAULT_STATUS_TEXT,
    WINDOW_MARGIN_X,
    WINDOW_MARGIN_Y,
)


class PetOverlay(QWidget):
    overlay_hidden = pyqtSignal()
    avatar_changed = pyqtSignal(str)
    tts_toggled = pyqtSignal(bool)
    interval_changed = pyqtSignal(int)
    model_changed = pyqtSignal(str)
    question_asked = pyqtSignal(str)   # NY: användaren ställde en fråga
    chat_mode_toggled = pyqtSignal(bool)  # NY: True = chat-läge, False = auto-läge

    def __init__(self) -> None:
        super().__init__()
        self._drag_pos = None
        self._tts_enabled = False
        self._chat_mode = False        # NY: håller koll på aktivt läge
        self._build_ui()
        self._position_bottom_right()

    def hide_for_capture(self) -> None:
        self.hide()
        QTimer.singleShot(CAPTURE_HIDE_DELAY_MS, self.overlay_hidden.emit)

    def _build_ui(self) -> None:
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.status_label = StatusLabel(DEFAULT_STATUS_TEXT)
        self.bubble = SpeechBubble(DEFAULT_BUBBLE_TEXT)
        self.avatar = AvatarWidget(DEFAULT_AVATAR_TEXT)

        # --- NY: Chat-inmatning ---
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ställ en fråga...")
        self.chat_input.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #888;
            }
        """)
        self.chat_input.returnPressed.connect(self._on_question_submitted)

        self.send_button = QPushButton("➤")
        self.send_button.setFixedSize(32, 32)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border: 1px solid #555;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #222;
            }
        """)
        self.send_button.clicked.connect(self._on_question_submitted)

        chat_row = QHBoxLayout()
        chat_row.setSpacing(4)
        chat_row.addWidget(self.chat_input)
        chat_row.addWidget(self.send_button)

        self.chat_widget = QWidget()
        self.chat_widget.setLayout(chat_row)
        self.chat_widget.hide()  # dold som standard

        layout.addWidget(self.status_label)
        layout.addWidget(self.bubble)
        layout.addWidget(self.avatar)
        layout.addWidget(self.chat_widget)

        self.setLayout(layout)
        self.adjustSize()

    def _on_question_submitted(self) -> None:
        """Anropas när användaren trycker Enter eller ➤-knappen."""
        question = self.chat_input.text().strip()
        if not question:
            return
        self.chat_input.clear()
        self.question_asked.emit(question)

    def _set_chat_mode(self, enabled: bool) -> None:
        """Visar eller döljer chat-inmatningen och uppdaterar läge."""
        self._chat_mode = enabled
        self.chat_widget.setVisible(enabled)
        self.adjustSize()
        self._position_bottom_right()
        self.chat_mode_toggled.emit(enabled)

    def _position_bottom_right(self) -> None:
        screen = QApplication.primaryScreen()
        if screen is None:
            geometry = QRect(0, 0, 1920, 1080)
        else:
            geometry = screen.availableGeometry()

        self.move(
            geometry.right() - self.width() - WINDOW_MARGIN_X,
            geometry.bottom() - self.height() - WINDOW_MARGIN_Y,
        )

    def update_status(self, text: str) -> None:
        self.status_label.set_status(text)

        if "Capturing" in text:
            self.avatar.set_state("capturing")
        elif "Thinking" in text:
            self.avatar.set_state("thinking")
        elif "Done" in text:
            self.avatar.set_state("talking")
        else:
            self.avatar.set_state("idle")

    def update_speech(self, text: str) -> None:
        self.bubble.set_text(text)
        self.adjustSize()
        self._position_bottom_right()

    def contextMenuEvent(self, event) -> None:
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #3a3a3a;
            }
            QMenu::separator {
                height: 1px;
                background: #555;
                margin: 4px 8px;
            }
        """)

        # --- Avatar-undermeny ---
        avatar_menu = QMenu("🐾 Välj avatar", self)
        avatar_menu.setStyleSheet(menu.styleSheet())
        for name, states in AVATARS.items():
            action = avatar_menu.addAction(f"{states['idle']} {name}")
            action.setData(("avatar", name))
        menu.addMenu(avatar_menu)

        menu.addSeparator()

        # --- Läge-toggle ---
        mode_label = "▶️ Byt till auto-läge" if self._chat_mode else "💬 Byt till chat-läge"
        mode_action = menu.addAction(mode_label)
        mode_action.setData(("mode", None))

        menu.addSeparator()

        # --- Intervall-undermeny (bara synlig i auto-läge) ---
        interval_menu = QMenu("⏱️ Intervall", self)
        interval_menu.setStyleSheet(menu.styleSheet())
        interval_menu.setEnabled(not self._chat_mode)
        for sec in [5, 10, 15, 30, 60]:
            action = interval_menu.addAction(f"{sec} sekunder")
            action.setData(("interval", sec))
        menu.addMenu(interval_menu)

        # --- Modell-undermeny ---
        model_menu = QMenu("🧠 AI-modell", self)
        model_menu.setStyleSheet(menu.styleSheet())
        available_models = get_installed_ollama_models()
        for model in available_models:
            action = model_menu.addAction(model)
            action.setData(("model", model))
        menu.addMenu(model_menu)

        menu.addSeparator()

        # --- TTS toggle ---
        tts_label = "🔇 Stäng av röst" if self._tts_enabled else "🔊 Slå på röst"
        tts_action = menu.addAction(tts_label)
        tts_action.setData(("tts", None))

        menu.addSeparator()

        # --- Avsluta ---
        quit_action = menu.addAction("❌ Avsluta")
        quit_action.setData(("quit", None))

        # --- Hantera val ---
        chosen = menu.exec(event.globalPos())

        if chosen is None:
            return

        data = chosen.data()
        if data is None:
            return

        kind, value = data

        if kind == "quit":
            QApplication.quit()

        elif kind == "tts":
            self._tts_enabled = not self._tts_enabled
            self.tts_toggled.emit(self._tts_enabled)

        elif kind == "avatar":
            self.avatar.set_avatar(value)
            self.avatar_changed.emit(value)

        elif kind == "interval":
            self.interval_changed.emit(value)

        elif kind == "model":
            self.model_changed.emit(value)

        elif kind == "mode":
            self._set_chat_mode(not self._chat_mode)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        if self._drag_pos is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event) -> None:
        self._drag_pos = None