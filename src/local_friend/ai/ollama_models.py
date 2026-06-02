import subprocess


FALLBACK_MODELS = [
    "llama3.2:latest",
    "moondream:latest",
    "minicpm-v:latest",
    "qwen3.5:0.8b",
    "qwen3.5:2b",
    "gemma4:e2b",
]


def get_installed_ollama_models() -> list[str]:
    """
    Hämtar installerade Ollama-modeller genom att köra 'ollama list'.

    Returnerar en fallback-lista om:
    - ollama inte finns i PATH
    - kommandot misslyckas
    - ingen modell kunde tolkas ut
    """
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=True,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return FALLBACK_MODELS.copy()

    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    if len(lines) <= 1:
        return FALLBACK_MODELS.copy()

    models: list[str] = []

    # Första raden är header, t.ex.:
    # NAME ID SIZE MODIFIED
    for line in lines[1:]:
        parts = line.split()
        if not parts:
            continue

        model_name = parts[0]

        if model_name not in models:
            models.append(model_name)

    return models or FALLBACK_MODELS.copy()