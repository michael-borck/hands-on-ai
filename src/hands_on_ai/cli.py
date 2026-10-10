"""
Meta CLI for hands-on-ai - provides version, configuration and module listing.
"""

import typer
from .commands import version, list, doctor, config, models

app = typer.Typer(help="AI Learning Lab Toolkit")

# Plain commands (single-action functions)
app.command(name="version", help="Display version information")(version.version)
app.command(name="list", help="List available modules")(list.list_modules)
app.command(name="doctor", help="Check environment and configuration")(doctor.doctor)

# Command groups (have their own subcommands)
app.add_typer(config.app, name="config", help="View or edit configuration")
app.add_typer(models.app, name="models", help="Manage and inspect LLM models")

# Add root command
@app.callback(invoke_without_command=True)
def root(ctx: typer.Context):
    """
    AI Learning Lab Toolkit - A modular toolkit for learning AI concepts.
    """
    # If no subcommand is provided, show list of modules
    if ctx.invoked_subcommand is None:
        list.list_modules()


if __name__ == "__main__":
    app()