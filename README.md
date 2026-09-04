# Local Friend

A privacy-first, local AI desktop assistant that analyses your screen activity and provides contextual commentary — without ever sending your data to the cloud.

Local Friend captures screenshots at regular intervals, processes them entirely in RAM, and sends them to a locally running Vision Language Model (VLM) via [Ollama](https://ollama.com). The result is a small, animated avatar that reacts to what is happening on your screen with short, personality-driven comments.

> ⚠️ **Privacy by design:** No screenshots are saved to disk. No data leaves your machine. Everything runs locally.

---

## Why Local Friend?

Modern AI assistants like ChatGPT, Microsoft Recall and Google Gemini offer powerful features, but most rely on cloud infrastructure. That means your screen content, your activity and your data are processed on someone else's servers.

Local Friend explores a different approach: **can a useful AI assistant be built entirely on the user's own hardware?**

This project demonstrates that the answer is yes — with the right architecture, trade-offs and a strong focus on privacy.

---

## Features

- 🔒 **100% local processing** — all image data stays on your computer.
- 🧠 **Vision Language Model integration** — analyses screen content using local VLMs via Ollama.
- 💾 **RAM-only image handling** — screenshots are never written to disk.
- 🪟 **Transparent desktop overlay** — a small, draggable avatar with speech bubbles.
- 🎭 **Persona system** — choose between multiple avatars with unique personalities.
- 🔊 **Offline Text-to-Speech** — the assistant can speak its comments out loud.
- 🖥️ **Cross-platform design** — developed for Linux (X11) and Windows using platform-independent libraries.
- ⚡ **Signal-driven architecture** — modular, thread-safe design using PyQt6 signals and the Mediator pattern.

---

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.11+ |
| GUI | PyQt6 |
| Screen capture | mss |
| Image processing | Pillow (PIL) |
| Local AI inference | Ollama |
| VLM model | Qwen 3.5 2B (or any vision-capable Ollama model) |
| Text-to-speech | pyttsx3 |
| Testing | pytest |
| Version control | Git + Conventional Commits |

---

## Architecture

Local Friend uses a modular, signal-driven architecture with a central `AppController` acting as a mediator between components:

```
┌─────────────────┐      signals       ┌─────────────────┐
│ AssistantWorker │ ─────────────────▶ │  AppController  │
│   (QThread)     │  status_update     │   (mediator)    │
│                 │  new_commentary    │                 │
│                 │  request_hide/show  │                 │
└─────────────────┘                    └────────┬────────┘
        ▲                                         │
        │ overlay_hidden                          │ signals
        │                                         ▼
┌─────────────────┐                    ┌─────────────────┐
│   PetOverlay    │ ◀──────────────────  │   TTSService    │
│   (PyQt6 UI)    │  update_status     │   (pyttsx3)     │
│                 │  update_speech     │                 │
└─────────────────┘                    └─────────────────┘
```

Key design decisions:

- **Mediator pattern:** Components communicate through signals rather than direct references, making the system easy to extend and test.
- **RAM-only image pipeline:** Screenshots are captured as raw bytes, converted to PIL images, encoded as base64 in memory, and sent to Ollama — never touching the filesystem.
- **Self-capture prevention:** The overlay hides itself before each screenshot to avoid the AI commenting on its own avatar.
- **Thread-safe coordination:** Uses Qt signals/slots combined with Python `threading.Event` for synchronous coordination between the worker thread and the UI thread.

---

## Installation

### Prerequisites

- Python 3.11 or newer
- [Ollama](https://ollama.com) installed and running
- A vision-capable model pulled in Ollama, for example:
  ```bash
  ollama pull qwen3.5:2b
  ```

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/itsabunny/Local-Friend.git
cd Local-Friend

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# .\venv\Scripts\Activate.ps1  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start Ollama (if not already running)
ollama serve

# 5. Run the application
python main.py
```

> **Note:** On Linux, an X11-based session is required. Wayland is not supported because its security model intentionally restricts external screen capture.

---

## Usage

Once the application is running:

1. A small avatar appears as an overlay on your screen.
2. Every 10 seconds, Local Friend captures a screenshot, analyses it, and displays a short comment.
3. Right-click the avatar to:
   - Switch between personas
   - Toggle Text-to-Speech on/off
   - Move the overlay

---

## Project Structure

```
Local-Friend/
├── local_friend/
│   ├── config.py               # Central configuration
│   ├── app/
│   │   └── controller.py       # Mediator / signal wiring
│   ├── ui/
│   ├── overlay.py          # Main overlay window
│   │   └── widgets.py          # Avatar, speech bubble, status label
│   ├── workers/
│   │   └── assistant_worker.py # Background capture & AI worker thread
│   ├── capture/
│   │   └── screen_capture.py   # mss-based screen capture
│   ├── services/
│   │   ├── commentary_service.py # Image prep, base64 encoding, deduplication
│   │   └── tts_service.py      # Offline text-to-speech
│   └── ai/
│       ├── ollama_client.py    # Local VLM communication
│       ├── ollama_models.py    # Installed Ollama models detection
│       └── prompts.py          # Persona system prompts
├── tests/                      # Unit tests
├── docs/                       # Thesis documentation and archived prototype
├── main.py                     # Application entry point
├── pyproject.toml              # Build & project metadata
├── requirements.txt            # Python dependencies
├── LICENSE.md                  # GNU General Public License v3.0
└── README.md                   # Project documentation
```

---

## Background

This project was developed as my degree project for the Java Developer programme at EC Utbildning, completed in June 2026.

The full thesis report (in Swedish) is available in the `docs/` folder and documents:

- The motivation behind local AI and privacy-first design
- The choice of technology stack
- The iterative development process (prototype → greenfield rebuild)
- Architectural decisions and trade-offs
- Results, limitations and future work

---

## Future Improvements

- Interactive question mode — let the user ask follow-up questions about the current screen.
- Local text metadata storage (SQLite) for history and journaling, without ever storing raw images.
- Systematic performance benchmarking across different model sizes and image resolutions.
- Packaging with PyInstaller for easy distribution.
- Extended platform testing on Windows and macOS.

---

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE.md) (GPLv3).

---

## Contact

Created by [Ninis Blomerus](https://github.com/itsabunny).

Feel free to open an issue or reach out if you have questions about the project.
