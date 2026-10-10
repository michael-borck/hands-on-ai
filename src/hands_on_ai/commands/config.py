"""
Config command for the hands-on-ai CLI - view or edit configuration.
"""

import typer
from rich import print
import json
from .. import config

app = typer.Typer(help="View or edit configuration")


@app.callback(invoke_without_command=True)
def show_config(ctx: typer.Context):
    """View or edit configuration."""
    if ctx.invoked_subcommand is not None:
        return
    config.ensure_config_dir()
    
    if not config.CONFIG_PATH.exists():
        # Create initial config
        print(f"Creating new config at {config.CONFIG_PATH}")
        current_config = config.load_config()  # Will load defaults
        config.save_config(current_config)
    
    # Display current config
    with open(config.CONFIG_PATH, "r") as f:
        config_data = json.load(f)
    
    print("\n[bold]Current Configuration:[/bold]")
    for key, value in config_data.items():
        print(f"  • {key}: {value}")
    
    print("\nTo edit configuration, open:\n" + str(config.CONFIG_PATH))


@app.command()
def init(force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing configuration")):
    """Initialize configuration with default values."""
    config.ensure_config_dir()
    
    if config.CONFIG_PATH.exists() and not force:
        print(f"[yellow]Configuration already exists at {config.CONFIG_PATH}[/yellow]")
        print("Use --force to overwrite with defaults")
        return
    
    # Load default config and save it
    default_config = config.load_default_config()
    config.save_config(default_config)
    
    print(f"[green]Default configuration initialized at {config.CONFIG_PATH}[/green]")
    print("\n[bold]Configuration:[/bold]")
    for key, value in default_config.items():
        print(f"  • {key}: {value}")


@app.command()
def get(key: str):
    """Get a specific configuration value."""
    cfg = config.load_config()
    if key in cfg:
        print(f"{key}: {cfg[key]}")
    else:
        print(f"[red]Key '{key}' not found in configuration[/red]")


@app.command()
def set(key: str, value: str):
    """Set a configuration value."""
    config.ensure_config_dir()
    
    # Load current config
    if config.CONFIG_PATH.exists():
        with open(config.CONFIG_PATH, "r") as f:
            cfg = json.load(f)
    else:
        cfg = config.load_default_config()
    
    # Special case for numeric values
    if value.isdigit():
        cfg[key] = int(value)
    elif value.lower() in ["true", "false"]:
        cfg[key] = value.lower() == "true"
    else:
        cfg[key] = value
    
    # Save updated config
    config.save_config(cfg)
    print(f"[green]Updated configuration:[/green] {key} = {cfg[key]}")