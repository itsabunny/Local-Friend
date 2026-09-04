import mss
from PIL import Image


class ScreenCaptureError(Exception):
    pass


def capture_primary_screen() -> Image.Image:
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            image = Image.frombytes(
                "RGB",
                screenshot.size,
                screenshot.rgb,
            )
            return image
    except Exception as exc:
        raise ScreenCaptureError(f"Failed to capture screen: {exc}") from exc