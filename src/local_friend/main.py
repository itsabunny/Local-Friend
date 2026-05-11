import sys
from PyQt6.QtWidgets import QApplication
from local_friend.ui.overlay import PetOverlay


def main() -> int:
    app = QApplication(sys.argv)
    overlay = PetOverlay()
    overlay.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())