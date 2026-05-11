# LocalDesktopPet

A cute, privacy-first desktop companion that "watches" your screen and provides witty, supportive, or sarcastic commentary using local Vision Language Models (VLM).

No cloud APIs, no subscriptions, and no data leaves your machine.

---

### The Philosophy

Most AI assistants are corporate, cloud-based, and sterile. **LocalDesktopPet** is designed to be:

* **Private:** Your screen data is stays on your disk and is processed by your local GPU/CPU.

* **Personal:** Uses customizable "personas" to act like a friend, a cat, or a grumpy senior developer.

* **Lightweight:** Designed to run in the background on standard laptops using small, efficient models.

---

### Features

* **Context-Aware Commentary:** Uses VLMs (like Qwen2-VL or Moondream) to actually "see" what you are doing.

* **Non-Intrusive Overlay:** A transparent, draggable PyQt6 window that stays on top of your work.

* **Smart Capturing:** Automatically hides itself before taking a screenshot so it doesn't "hallucinate" about its own existence.

* **Asynchronous Processing:** Background threading ensures your PC doesn't freeze while the AI is "thinking."

---

### Hardware & Performance

Since this is **100% Local AI**, performance depends entirely on your hardware:

* **RAM/VRAM:** Minimum 8GB (Total System RAM). 16GB+ recommended for smoother multi-tasking.

* **CPU/GPU:** Works best on systems with integrated or dedicated GPUs supported by Ollama.

* **Resolution:** Higher screen resolutions require more processing. The script automatically downscales images to maintain speed.

* **Performance Expectation:** On a standard modern laptop (non-gaming), expect 5-8 seconds for a response using a 2B parameter model.

---

### Getting Started

#### 1\. Prerequisites

* **Linux:** Currently optimized for **Debian/KDE** environments.

* **Display Server:** **X11 is recommended.** Wayland users may experience issues with window dragging and "Always on Top" behavior.

* **Ollama:** Install from [ollama.com](https://ollama.com).

#### 2\. Install Dependencies

```bash
# Install Python dev headers and screen capture tool
sudo apt install python3-dev spectacle

# Install Python libraries
pip install PyQt6 Pillow ollama
```

#### 3\. Setup the AI Model

Pull a vision-capable model (we recommend Qwen2-VL 2B for the best speed/accuracy balance):

```bash
ollama pull qwen2-vl:2b
```

_Note: Update the `MODEL` variable in `script.py` if you use a different model._

#### 4\. Run the Pet

```bash
python script.py
```

---

### Current Constraints

* **Platform Specific:** Currently uses `spectacle` command-line flags for screen capture (KDE-centric).

* **Session Type:** Overlay interaction (dragging) is most stable on X11 sessions.

* **Context Window:** The pet currently sees the "now," but doesn't yet remember what happened 5 minutes ago.

---

### Roadmap

* \[ \] **State-Based Animations:** Mouth movement during "talking" state and blinking during "idle."

* \[ \] **Cross-Platform Support:** Move to a platform-agnostic capture library (like `mss` for X11).

* \[ \] **Long-Term Memory:** Feed previous commentary back into the prompt for continuous conversation.

* \[ \] **Activity Triggers:** Only trigger commentary when significant screen changes are detected.