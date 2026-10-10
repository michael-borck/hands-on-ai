"""
CLI for the vision module.
"""

from typing import Optional

import typer
from rich import print

from .describe import describe

app = typer.Typer(help="Ask a vision model about an image")


@app.callback(invoke_without_command=True)
def ask(
    image: str = typer.Argument(..., help="Path or URL of the image."),
    prompt: str = typer.Argument(
        "Describe this image.", help="Question or instruction about the image."
    ),
    model: Optional[str] = typer.Option(None, help="Vision model (defaults to config)."),
):
    """Ask a vision-language model about an image."""
    print(describe(image, prompt=prompt, model=model))


if __name__ == "__main__":
    app()
