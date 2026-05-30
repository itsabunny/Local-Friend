import sys
from PyQt6.QtWidgets import QApplication
from local_friend.app.controller import AppController


def main() -> int:
    app = QApplication(sys.argv)
    controller = AppController()
    controller.start()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())