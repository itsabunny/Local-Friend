"""
Local Desktop Pet

A small PyQt overlay that periodically captures the screen, sends it to a local
vision-capable Ollama model, and displays short playful commentary in a floating
speech bubble.

Currently tested on Linux with X11. The window hides itself before each capture
to avoid appearing in the screenshot.
"""

import sys
import subprocess
import time
import os
import random
from pathlib import Path
from PIL import Image
import ollama

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPoint, QRect
from PyQt6.QtGui import QFont

# The Ollama model to use for commentary. You can change this to your preferred VLM model.
MODEL = "qwen3.5:2b"

# --- WORKER THREAD (asynchronous, handles background tasks) ---
class AssistantWorker(QThread):
    """Background thread that captures the screen, processes it with the VLM, and emits signals to update the UI."""
    new_message = pyqtSignal(str)
    status_update = pyqtSignal(str)
    hide_for_capture = pyqtSignal()   # Tell UI to hide
    show_after_capture = pyqtSignal() # Tell UI to show again

    def run(self):
        """Main loop: capture screen every 20 seconds, get commentary, and emit updates."""
        last_run_time = time.time() - 20
        last_commentary = ""

        while True:
            current_time = time.time()
            if current_time - last_run_time > 20: # Run every 20 seconds
                self.status_update.emit("📸 Capturing...")

                # Hide window, wait a moment for it to disappear, then capture
                self.hide_for_capture.emit()
                self.msleep(300)  # 300ms for window to hide

                screenshot = self.capture_screen()
                self.show_after_capture.emit()

                # Process screenshot with VLM and get commentary
                if screenshot:
                    self.status_update.emit("🤔 Thinking...")
                    screenshot = self.prepare_image_for_vlm(screenshot) # Resize for efficiency and model limits
                    commentary = self.get_commentary(screenshot) # Get commentary from VLM

                    # Skip if too similar to last message (simple repeat check)
                    if commentary and commentary.strip() != last_commentary.strip():
                        last_commentary = commentary
                        self.new_message.emit(commentary)
                        print(f"\n🐱 Pet: {commentary}")
                    else:
                        print("(Skipped repeated commentary)")
                        self.status_update.emit("💤 Same as before, skipping...")
                else:
                    self.status_update.emit("⚠️ Capture failed")

                last_run_time = time.time()
            else:
                # Update status with countdown until next capture
                remaining = int(20 - (current_time - last_run_time))
                if remaining > 0:
                    print(f"Waiting... {remaining:2d}s until next capture", end="\r")
                else:
                    print("") # new line after countdown reaches zero to keep console output clean
                self.status_update.emit(f"💤 Next in {remaining}s")

            self.msleep(500)

    # TODO: Replace with platform agnostic capture method if possible. This currently uses Spectacle which is KDE-specific.
    def capture_screen(self):
        """Captures the screen using Spectacle (needed for Wayland). Adjust this method if using a different OS or capture tool."""
        print("Capturing screen...")
        Path("captures").mkdir(exist_ok=True)
        temp_path = Path("captures/temp_ui.png")
        env = os.environ.copy() # Inherit environment to ensure DISPLAY and WAYLAND_DISPLAY are available for spectacle
        try:
            # Platform-specific: uses Spectacle for Wayland. Adjust command if using a different OS or capture tool.
            result = subprocess.run(
                ["spectacle", "-b", "-n", "-o", str(temp_path)],
                capture_output=True, text=True, timeout=10, env=env
            )

            # Prevent file lock issues by checking return code and existence before opening
            if result.returncode == 0 and temp_path.exists():
                print("Screen captured successfully.")

                return Image.open(temp_path).copy()  # .copy() releases file lock
        except Exception as e:
            print(f"Capture error: {e}")
        return None

    def prepare_image_for_vlm(self, img, max_width=896):
        """Resizes the image if it's wider than the model's maximum input width. This is a simple heuristic for qwen3.5's limits."""
        img = img.convert("RGB") # Prevent issues with alpha channels
        if img.width > max_width:
            h = int(img.height * max_width / img.width)
            img = img.resize((max_width, h), Image.Resampling.LANCZOS)
        print(f"Prepared image for VLM: {img.width}x{img.height}")
        return img

    def get_commentary(self, image):
        """Sends the image to the VLM and gets a brief, playful commentary. Uses a random persona for fun variation."""
        print("Getting commentary from VLM...")
        temp_path = Path("temp_ui_vlm.png") # Save a temporary copy for the VLM to read for easier usage path.
        image.save(temp_path, "PNG")
        try:
            # Used to simulate different "personalities" in the commentary. You can customize these or add more for fun variety.
            personas = [
                "You're a witty friend looking over the user's shoulder.",
                "You're a supportive friend who notices small things.",
                "You're a helpful but sarcastic coding buddy.",
                "You're a cat sitting on the desk watching the screen."
            ]
            persona = random.choice(personas)
            print(f"Using persona: {persona}")

            # Create a client with a 30-second timeout to prevent hanging if the model has issues. Adjust as needed based on your model's performance.
            client = ollama.Client(timeout=30.0)

            # Main VLM call: sends the image with a system prompt to guide the style of commentary. Adjust options as needed for your model.
            response = client.chat(
                model=MODEL,
                messages=[{ # Tone and style guidance
                    'role': 'system',
                    'content': persona
                }, { # Type of commentary
                    'role': 'user',
                    'content': "Make a brief, playful comment about what's on this screen. 1 short sentence only.",
                    'images': [str(temp_path)]
                }],
                keep_alive="5m", # Keep the model loaded for faster responses if called again within 5 minutes
                think=False, # Disabled because this model/backend produced unstable or empty responses with thinking enabled.
                options={ # Conservative generation settings to keep responses short and improve performance on low VRAM systems.
                    "num_predict": 35,
                    "temperature": 0.75,
                    "top_p": 0.9,
                    "num_ctx": 2048, # Prevent memory issues with low VRAM. Dependent on image size and model limits.
                }
            )
            temp_path.unlink(missing_ok=True) # Clean up temp image file
            return response['message']['content'].strip() # Return the commentary text, stripping any extra whitespace
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"


# --- UI WINDOW (overlay that displays the pet and commentary) ---
class PetOverlay(QWidget):
    """Main UI window that shows the pet avatar, speech bubble, and status. It listens to signals from the AssistantWorker to update the display."""
    def __init__(self):
        """Initializes the UI and starts the background worker thread."""
        super().__init__()
        self._drag_pos = None
        self.init_ui()

        self.worker = AssistantWorker()
        self.worker.new_message.connect(self.update_speech)
        self.worker.status_update.connect(self.update_status)
        self.worker.hide_for_capture.connect(self.hide)   # Hide before capture
        self.worker.show_after_capture.connect(self.show) # Show after capture
        self.worker.start()

    def init_ui(self):
        """Sets up the UI elements and styles for the pet overlay window."""
        self.setWindowFlags( 
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool # Prevent taskbar entry
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # Transparent background

        # Outer layout to stack widgets vertically
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Status label
        self.status_label = QLabel("Initializing...")
        self.status_label.setStyleSheet("color: #aaa; font-size: 10px; background: transparent;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Speech bubble
        self.bubble = QLabel("Hi! I'm watching... 👀")
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

        # Avatar
        self.avatar = QLabel("🐱")
        self.avatar.setFont(QFont("Noto Color Emoji", 36))
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar.setStyleSheet("background: transparent;")

        # Add widgets to layout and set the main layout
        layout.addWidget(self.status_label)
        layout.addWidget(self.bubble)
        layout.addWidget(self.avatar)
        self.setLayout(layout)
        self.adjustSize()

        # Position: bottom-right, above taskbar
        screen = QApplication.primaryScreen()
        if screen is None:
            geometry = QRect(0, 0, 1920, 1080)
        else:
            geometry = screen.availableGeometry()
        self.move(geometry.right() - self.width() - 20, geometry.bottom() - self.height() - 20)

    def update_speech(self, text):
        """Updates the speech bubble text and repositions the window to stay anchored to the bottom-right after resizing."""
        self.bubble.setText(text)
        self.adjustSize()
        # Re-anchor to bottom-right after resize
        screen = QApplication.primaryScreen()
        if screen is None:
            geometry = QRect(0, 0, 1920, 1080)
        else:
            geometry = screen.availableGeometry()
        self.move(geometry.right() - self.width() - 20, geometry.bottom() - self.height() - 20) # Moves to bottom-right with a 20px margin. Design choice to keep it away from screen edges and non-intrusive.

    def update_status(self, text):
        """Updates the status label text to show current activity or countdown until next capture."""
        self.status_label.setText(text)

    # --- DRAG FUNCTIONALITY ---
    def mousePressEvent(self, a0):
        """Allows the user to click and drag the window to reposition it. Stores the initial click position relative to the window."""
        if a0.button() == Qt.MouseButton.LeftButton:  # type: ignore
            self._drag_pos = a0.globalPosition().toPoint() - self.frameGeometry().topLeft()  # type: ignore
            a0.accept()  # type: ignore

    def mouseMoveEvent(self, a0):
        """Moves the window as the user drags it, based on the initial click position. Only moves if the left mouse button is held down."""
        if self._drag_pos is not None and a0.buttons() == Qt.MouseButton.LeftButton:  # type: ignore
            self.move(a0.globalPosition().toPoint() - self._drag_pos)  # type: ignore
            a0.accept()  # type: ignore

    def mouseReleaseEvent(self, a0):
        """Resets the drag position when the user releases the mouse button, ending the drag operation."""
        self._drag_pos = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = PetOverlay()
    pet.show()
    sys.exit(app.exec()) # Start the Qt event loop