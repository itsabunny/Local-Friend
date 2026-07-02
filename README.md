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
