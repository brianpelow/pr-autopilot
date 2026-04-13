"""label command — suggest PR labels based on change type."""

from __future__ import annotations

import typer
from rich.console import Console

from prautopilot.core.diff import get_diff
from prautopilot.core.labels import suggest_labels
from prautopilot.core.github import push_pr_labels

label_app = typer.Typer(help="Suggest and apply PR labels.")
console = Console()


@label_app.callback(invoke_without_command=True)
def label(
    ctx: typer.Context,
    base: str = typer.Option("main", "--base", "-b", help="Base branch to diff against"),
    push: bool = typer.Option(False, "--push/--no-push", help="Apply labels to open PR"),
) -> None:
    """Suggest labels for your PR based on what changed."""
    if ctx.invoked_subcommand is not None:
        return

    diff = get_diff(base_branch=base)

    if diff.is_empty:
        console.print("[yellow]No changes detected.[/yellow]")
        raise typer.Exit(1)

    labels = suggest_labels(diff)
    console.print(f"\n[bold]Suggested labels:[/bold] {', '.join(f'[cyan]{l}[/cyan]' for l in labels)}\n")

    if push:
        success = push_pr_labels(labels)
        if success:
            console.print("[green]✓ Labels applied to PR[/green]")
        else:
            console.print("[yellow]Could not apply labels — is there an open PR for this branch?[/yellow]")