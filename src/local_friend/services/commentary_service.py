import io
import base64
from PIL import Image

from local_friend.ai.ollama_client import OllamaClient
from local_friend.ai.prompts import get_random_persona, DEFAULT_QUERY
from local_friend.config import MAX_IMAGE_WIDTH


def prepare_image_for_model(image: Image.Image) -> Image.Image:
    image = image.convert("RGB")
    if image.width > MAX_IMAGE_WIDTH:
        new_height = int(image.height * MAX_IMAGE_WIDTH / image.width)
        image = image.resize((MAX_IMAGE_WIDTH, new_height), Image.Resampling.LANCZOS)
    return image


def _pil_to_base64(image: Image.Image) -> str:
    """Konverterar PIL-bild till base64-sträng i RAM – ingen fil skrivs till disk."""
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


class CommentaryService:
    def __init__(self) -> None:
        self.ai_client = OllamaClient()
        self.last_commentary = ""

    def get_new_commentary(self, pil_image: Image.Image) -> str | None:
        persona = get_random_persona()
        image_b64 = _pil_to_base64(pil_image)

        commentary = self.ai_client.get_vision_commentary(
            image_b64, persona, DEFAULT_QUERY
        ).strip()

        if not commentary or commentary == self.last_commentary:
            return None

        self.last_commentary = commentary
        return commentary