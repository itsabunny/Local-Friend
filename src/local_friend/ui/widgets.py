from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


AVATARS = {
    "Smiley": {
        "idle":      "😊",
        "thinking":  "🤔",
        "capturing": "📸",
        "talking":   "😀",
    },
    "Anka": {
        "idle":      "🦆",
        "thinking":  "🦆",
        "capturing": "🦆",
        "talking":   "🦆",
    },
    "Kanin": {
        "idle":      "🐰",
        "thinking":  "🐰",
        "capturing": "🐰",
        "talking":   "🐰",
    },
    "Apa": {
        "idle":      "🐵",
        "thinking":  "🙈",
        "capturing": "🙉",
        "talking":   "🙊",
    },
    "Uggla": {
        "idle":      "🦉",
        "thinking":  "🦉",
        "capturing": "🦉",
        "talking":   "🦉",
    },
}

class StatusLabel(QLabel):
    def __init__(self, text: str):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            "color: #aaa; font-size: 10px; background: transparent;"
        )

    def set_status(self, text: str) -> None:
        self.setText(text)


class SpeechBubble(QLabel):
    def __init__(self, text: str):
        super().__init__(text)
        self.setWordWrap(True)
        self.setMinimumWidth(180)
        self.setMaximumWidth(280)
        self.setStyleSheet("""
            background-color: rgba(30, 30, 30, 220);
            border: 1px solid #888;
            border-radius: 12px;
            padding: 10px 14px;
            color: white;
            font-size: 13px;
        """)

    def set_text(self, text: str) -> None:
        self.setText(text)


class AvatarWidget(QLabel):
    def __init__(self, avatar_name: str = "Smiley"):
        self._states = AVATARS[avatar_name]
        super().__init__(self._states["idle"])
        self.state = "idle"
        self.setFont(QFont("Noto Color Emoji", 36))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background: transparent;")

    def set_avatar(self, avatar_name: str) -> None:
        self._states = AVATARS[avatar_name]
        self.set_state(self.state)  # uppdatera direkt med nuvarande state

    def set_state(self, state: str) -> None:
        self.state = state
        self.setText(self._states.get(state, self._states["idle"]))