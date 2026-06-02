from PyQt6.QtCore import Qt, QRect, QTimer, pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QApplication, QMenu

from local_friend.ui.widgets import SpeechBubble, StatusLabel, AvatarWidget, AVATARS
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

    def __init__(self) -> None:
        super().__init__()
        self._drag_pos = None
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

        layout.addWidget(self.status_label)
        layout.addWidget(self.bubble)
        layout.addWidget(self.avatar)

        self.setLayout(layout)
        self.adjustSize()

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

        avatar_menu = QMenu("🐾 Välj avatar", self)
        avatar_menu.setStyleSheet(menu.styleSheet())

        for name, states in AVATARS.items():
            action = avatar_menu.addAction(f"{states['idle']} {name}")
            action.setData(name)

        menu.addMenu(avatar_menu)
        menu.addSeparator()
        quit_action = menu.addAction("❌ Avsluta")

        action = menu.exec(event.globalPos())

        if action is None:
            return

        if action == quit_action:
            QApplication.quit()
            return

        avatar_name = action.data()
        if avatar_name:
            self.avatar.set_avatar(avatar_name)
            self.avatar_changed.emit(avatar_name)

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