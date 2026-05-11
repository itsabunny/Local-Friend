from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication

from local_friend.config import (
    DEFAULT_AVATAR_TEXT,
    DEFAULT_BUBBLE_TEXT,
    DEFAULT_STATUS_TEXT,
    WINDOW_MARGIN_X,
    WINDOW_MARGIN_Y,
)


class PetOverlay(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._drag_pos = None
        self._build_ui()
        self._position_bottom_right()

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

        self.status_label = QLabel(DEFAULT_STATUS_TEXT)
        self.status_label.setStyleSheet(
            "color: #aaa; font-size: 10px; background: transparent;"
        )
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.bubble = QLabel(DEFAULT_BUBBLE_TEXT)
        self.bubble.setWordWrap(True)
        self.bubble.setMinimumWidth(180)
        self.bubble.setMaximumWidth(280)
        self.bubble.setStyleSheet("""
            background-color: rgba(30, 30, 30, 220);
            border: 1px solid #888;
            border-radius: 12px;
            padding: 10px 14px;
            color: white;
            font-size: 13px;
        """)

        self.avatar = QLabel(DEFAULT_AVATAR_TEXT)
        self.avatar.setFont(QFont("Noto Color Emoji", 36))
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar.setStyleSheet("background: transparent;")

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
        self.status_label.setText(text)

    def update_speech(self, text: str) -> None:
        self.bubble.setText(text)
        self.adjustSize()
        self._position_bottom_right()

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