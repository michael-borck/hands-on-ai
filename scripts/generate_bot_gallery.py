#!/usr/bin/env python3

import inspect
import re
import csv
from collections import defaultdict
from io import StringIO
import typer
from typing import Optional
from pathlib import Path

# Import from ailabkit package
import ailabkit
from ailabkit.chat.personalities import bots

BOT_TEMPLATE = '''def your_bot_name(prompt):
    """
    🤖 Your Bot Title

    One-line summary of your bot's personality.

    ```python
    from ailabkit.chat import your_bot_name
    response = your_bot_name("Ask me anything")
    print(response)
    ```

    **Example Output:**
    ```
    Your awesome response goes here.
    ```

    **Educational Uses:**
    - Example usage 1
    - Example usage 2

    Args:
        prompt (str): The user's input text or question.

    Returns:
        str: The bot's response in its unique personality style.
    """
    return get_response(prompt, system="Describe your bot's behavior here.", personality="yourpersonality")
'''

HEADER = """# 🤖 Hands-On AI Personality Gallery

This gallery lists all available personality bots in Hands-On AI's chat module. Each bot is just `get_response` with a fixed system prompt. See [Understanding Chat & Bots](chat-concepts.md). Each bot can be called with a prompt and will respond in its own unique style.

Below you'll find each bot's name and its docstring, which includes usage examples, educational applications, and example responses (as written in the docstring).

---
"""

def is_bot_func(obj):
    return callable(obj) and obj.__name__.endswith('_bot')

def extract_bots():
    bot_list = []
    # Check directly in the bots module
    for name in dir(bots):
        obj = getattr(bots, name)
        if is_bot_func(obj):
            doc = inspect.getdoc(obj)
            bot_list.append((name, doc))
            
    # Also check if any bots are directly exported at the module level
    for name in dir(ailabkit.chat):
        obj = getattr(ailabkit.chat, name)
        if is_bot_func(obj):
            doc = inspect.getdoc(obj)
            if (name, doc) not in bot_list:  # Avoid duplicates
                bot_list.append((name, doc))
                
    return bot_list

def parse_educational_tags(doc):
    if not doc:
        return []
    match = re.search(r"\*\*Educational Uses:\*\*(.*?)\n\n", doc, re.DOTALL)
    if match:
        tags = re.findall(r"- (.+)", match.group(1))
        return [t.strip() for t in tags]
    return []

def generate_markdown(bots, lint=False, include_header=True, flat=False):
    if lint:
        return "\n".join([f"⚠️ `{name}` is missing a docstring." for name, doc in bots if not doc])

    lines = [HEADER] if include_header else []

    if flat:
        for name, doc in sorted(bots):
            if doc:
                lines.append(f"### `{name}`\n{doc}\n")
    else:
        tag_sections = defaultdict(list)
        for name, doc in bots:
            if doc:
                tags = parse_educational_tags(doc)
                if not tags:
                    tag_sections["Uncategorized"].append((name, doc))
                else:
                    for tag in tags:
                        tag_sections[tag].append((name, doc))

        for tag, items in sorted(tag_sections.items()):
            lines.append(f"\n## 🏷️ {tag}\n")
            for name, doc in sorted(items):
                lines.append(f"### `{name}`\n{doc}\n")

    return "\n".join(lines)

def generate_csv(bots):
    csv_output = StringIO()
    writer = csv.writer(csv_output)
    writer.writerow(["Bot Name", "Educational Tag"])

    for name, doc in bots:
        if not doc:
            continue
        tags = parse_educational_tags(doc)
        if not tags:
            writer.writerow([name, "Uncategorized"])
        else:
            for tag in tags:
                writer.writerow([name, tag])

    return csv_output.getvalue()

app = typer.Typer(help="Generate or lint AiLabKit bot gallery")

@app.command()
def generate(
    lint: bool = typer.Option(
        False,
        "--lint",
        help="Check for missing docstrings only"
    ),
    out: Optional[Path] = typer.Option(
        None,
        "--out",
        "-o",
        help="Path to output file. If not set, prints to stdout"
    ),
    template: bool = typer.Option(
        False,
        "--template",
        "-t",
        help="Print a template for creating a new bot"
    ),
    no_header: bool = typer.Option(
        False,
        "--no-header",
        help="Exclude the header section from output"
    ),
    flat: bool = typer.Option(
        False,
        "--flat",
        "-f",
        help="Disable section grouping and print all bots in one list"
    ),
    csv_output: bool = typer.Option(
        False,
        "--csv",
        "-c",
        help="Output a CSV file instead of Markdown"
    ),
):
    """Generate a gallery of available bots with their documentation."""
    if template:
        typer.echo(BOT_TEMPLATE)
        raise typer.Exit()

    bot_list = extract_bots()

    if csv_output:
        output = generate_csv(bot_list)
    else:
        output = generate_markdown(bot_list, lint=lint, include_header=not no_header, flat=flat)

    if out:
        out.write_text(output)
        typer.echo(f"✅ Bot gallery written to {out}")
    else:
        typer.echo(output)

if __name__ == "__main__":
    app()
