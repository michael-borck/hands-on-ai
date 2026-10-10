"""
Describe images with a vision-language model (VLM).

Underneath, a VLM call is a normal chat call: the image is encoded into the
user message alongside your text, and the model replies in plain language.
That is the whole idea -- one model, one more kind of input.
"""

import base64
import mimetypes
from pathlib import Path

from ..chat.get_response import chat_completion
from ..config import get_vision_model

DEFAULT_PROMPT = "Describe this image."

_SYSTEM = "You are a helpful assistant that answers questions about images."

# Image types we know how to label in a data URL.
_MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
}


def _image_url(image: str) -> str:
    """
    Turn an image reference into the URL form the API expects.

    Web URLs pass through untouched. Local files are read and inlined as a
    ``data:`` URL (base64 text that carries the image bytes with it).
    """
    if image.startswith(("http://", "https://")):
        return image

    path = Path(image)
    if not path.is_file():
        raise FileNotFoundError(f"Image file not found: {image}")

    mime = _MIME_TYPES.get(path.suffix.lower()) or mimetypes.guess_type(str(path))[0]
    if not mime or not mime.startswith("image/"):
        mime = "image/png"  # providers are forgiving; the bytes matter most
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def describe(
    image: str,
    prompt: str = DEFAULT_PROMPT,
    model: str | None = None,
    retries: int = 2,
    timeout: float = 120,
) -> str:
    """
    Ask a vision-language model about an image.

    Args:
        image: Path to a local image file, or an http(s) URL.
        prompt: What to do with the image, e.g. "What's funny about this?"
        model: Vision model to use (defaults to the ``vision_model`` config
            setting, which is ``moondream`` unless you override it).
        retries: Number of attempts before giving up.
        timeout: Request timeout in seconds. Generous by default because
            image models are slower than text models.

    Returns:
        str: The model's answer, or an error message string in the same
        style as :func:`hands_on_ai.chat.get_response`.
    """
    if model is None:
        model = get_vision_model()

    try:
        url = _image_url(image)
    except (FileNotFoundError, OSError) as e:
        return f"❌ Error: {e}"

    messages = [
        {"role": "system", "content": _SYSTEM},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": url}},
            ],
        },
    ]
    reply, _ = chat_completion(messages, model=model, retries=retries, timeout=timeout)
    return reply
