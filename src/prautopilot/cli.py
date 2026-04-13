"""pr-autopilot CLI entry point."""

from __future__ import annotations

import typer
from rich.console import Console

from prautopilot import __version__
from prautopilot.commands.generate import generate_app
from prautopilot.commands.hook import hook_app
from prautopilot.commands.review import review_app
from prautopilot.commands.label import label_app

app = typer.Typer(
    name="pr-autopilot",
    help="AI-generated PR descriptions for regulated industries engineering teams.",
    add_completion=True,
    rich_markup_mode="rich",
)
console = Console()

app.add_typer(generate_app, name="generate")
app.add_typer(hook_app, name="hook")
app.add_typer(review_app, name="review")
app.add_typer(label_app, name="label")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="Show version and exit."),
) -> None:
    """pr-autopilot — AI-generated PR descriptions for regulated industries."""
    if version:
        console.print(f"pr-autopilot v{__version__}")
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())