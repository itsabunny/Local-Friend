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
    Retrieves installed Ollama models by running 'ollama list'.

    Returns a fallback list if:
    - ollama is not in PATH
    - the command fails
    - no model could be parsed
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

    # First line is the header, e.g.:
    # NAME ID SIZE MODIFIED
    for line in lines[1:]:
        parts = line.split()
        if not parts:
            continue

        model_name = parts[0]

        if model_name not in models:
            models.append(model_name)

    return models or FALLBACK_MODELS.copy()