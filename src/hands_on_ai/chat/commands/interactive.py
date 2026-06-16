"""
Interactive command for the chat CLI.
"""

import typer
from rich import print
import requests
from ..bots import get_bot
from ..get_response import set_stream_printing
from ...config import get_server_url

app = typer.Typer(help="Start interactive REPL")


def check_server():
    """Check if Ollama server is running."""
    url = get_server_url()
    try:
        r = requests.get(f"{url}/api/tags", timeout=2)
        if r.status_code == 200:
            return True
    except Exception:
        pass
    return False


@app.callback(invoke_without_command=True)
def interactive():
    """Start interactive REPL (no memory)."""
    current_bot_name = "friendly_bot"

    if not check_server():
        print("[red]❌ Ollama server is not reachable. Run `chat doctor` for help.[/red]")
        raise typer.Exit(1)

    print("\n🤖 [bold]Chat CLI[/bold]: stateless REPL, no memory between prompts.")
    print("Type /help for commands.\n")

    # Stream responses token-by-token so you can watch the model generate.
    set_stream_printing(True)

    bot = get_bot(current_bot_name)
    if not bot:
        print(f"[red]❌ Default bot '{current_bot_name}' not found.[/red]")
        return

    while True:
        try:
            user_input = input("💬 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Exiting Chat.")
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            command, *args = user_input[1:].split()
            if command == "exit":
                print("👋 Goodbye!")
                break
            elif command == "help":
                print("""
🤖 [bold]Chat CLI[/bold]: stateless REPL, no memory between prompts.
📖 [bold]Available commands:[/bold]
  /help              Show this help message
  /exit              Exit the REPL
  /bots              List all available bot personalities
  /personality NAME  Switch to another bot personality (e.g., /personality pirate)
  /doctor            Check Ollama server status
                """)
            elif command == "bots":
                from .bots import list_bots
                list_bots()
            elif command == "doctor":
                from .doctor import doctor
                doctor()
            elif command == "personality":
                if not args:
                    print("[red]⚠️ Usage: /personality NAME[/red]")
                else:
                    name = args[0]
                    new_bot = get_bot(name)
                    if new_bot:
                        current_bot_name = name
                        bot = new_bot
                        print(f"✅ Switched to bot: [cyan]{name}[/cyan]")
                    else:
                        print(f"[red]❌ No bot named '{name}'. Try /bots[/red]")
            else:
                print(f"[red]⚠️ Unknown command: /{command}[/red]")
        else:
            print("🤖 ", end="")
            bot(user_input)   # streams token-by-token (live printing enabled)
            print()