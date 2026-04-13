"""hook command — install pr-autopilot as a git hook."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

hook_app = typer.Typer(help="Manage git hook integration.")
console = Console()

HOOK_SCRIPT = """#!/bin/sh
# pr-autopilot git hook
# Runs pr-autopilot generate before push to document your changes
pr-autopilot generate --dry-run
"""


@hook_app.command("install")
def hook_install(
    repo_path: Path = typer.Option(Path("."), "--repo", help="Path to git repo"),
) -> None:
    """Install pr-autopilot as a git pre-push hook."""
    hook_path = repo_path / ".git" / "hooks" / "pre-push"

    if hook_path.exists():
        console.print(f"[yellow]Hook already exists at {hook_path}[/yellow]")
        overwrite = typer.confirm("Overwrite?")
        if not overwrite:
            raise typer.Exit()

    hook_path.write_text(HOOK_SCRIPT)
    hook_path.chmod(0o755)
    console.print(f"[green]✓ Hook installed at {hook_path}[/green]")
    console.print("[dim]pr-autopilot generate will run before every push[/dim]")


@hook_app.command("uninstall")
def hook_uninstall(
    repo_path: Path = typer.Option(Path("."), "--repo", help="Path to git repo"),
) -> None:
    """Remove the pr-autopilot git hook."""
    hook_path = repo_path / ".git" / "hooks" / "pre-push"

    if not hook_path.exists():
        console.print("[yellow]No hook found.[/yellow]")
        raise typer.Exit()

    hook_path.unlink()
    console.print(f"[green]✓ Hook removed from {hook_path}[/green]")