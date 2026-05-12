import ollama
from local_friend.config import OLLAMA_MODEL, OLLAMA_TIMEOUT_SECONDS, OLLAMA_KEEP_ALIVE

class OllamaClient:
    def __init__(self):
        # Vi skapar en klient med timeout för att appen inte ska hänga sig om Ollama är segt
        self.client = ollama.Client(timeout=OLLAMA_TIMEOUT_SECONDS)

    def get_vision_commentary(self, image_path, system_prompt, user_query):
        """Skickar en bild och prompt till Ollama och returnerar svar."""
        try:
            response = self.client.chat(
                model=OLLAMA_MODEL,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_query, 'images': [image_path]}
                ],
                keep_alive=OLLAMA_KEEP_ALIVE,
                options={"num_predict": 35, "temperature": 0.75}
            )
            return response['message']['content'].strip()
        except Exception as e:
            return f"Error: {str(e)}"