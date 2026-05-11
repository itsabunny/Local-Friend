from PIL import Image

from local_friend.config import MAX_IMAGE_WIDTH


def prepare_image_for_model(image: Image.Image) -> Image.Image:
    image = image.convert("RGB")

    if image.width > MAX_IMAGE_WIDTH:
        new_height = int(image.height * MAX_IMAGE_WIDTH / image.width)
        image = image.resize((MAX_IMAGE_WIDTH, new_height), Image.Resampling.LANCZOS)

    return image