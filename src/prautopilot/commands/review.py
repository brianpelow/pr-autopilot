"""review command — suggest reviewers based on changed files."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from prautopilot.core.diff import get_diff
from prautopilot.core.reviewers import suggest_reviewers

review_app = typer.Typer(help="Suggest PR reviewers based on changed files.")
console = Console()


@review_app.callback(invoke_without_command=True)
def review(
    ctx: typer.Context,
    base: str = typer.Option("main", "--base", "-b", help="Base branch to diff against"),
    top: int = typer.Option(3, "--top", "-n", help="Number of reviewers to suggest"),
) -> None:
    """Suggest reviewers based on who last touched the changed files."""
    if ctx.invoked_subcommand is not None:
        return

    diff = get_diff(base_branch=base)

    if diff.is_empty:
        console.print("[yellow]No changes detected.[/yellow]")
        raise typer.Exit(1)

    reviewers = suggest_reviewers(diff, top_n=top)

    if not reviewers:
        console.print("[yellow]No reviewer suggestions — not enough git history.[/yellow]")
        return

    table = Table(title="Suggested reviewers", border_style="dim")
    table.add_column("Email", style="cyan")
    table.add_column("Reason", style="dim")

    for reviewer in reviewers:
        table.add_row(reviewer, "Recently modified changed files")

    console.print(table)