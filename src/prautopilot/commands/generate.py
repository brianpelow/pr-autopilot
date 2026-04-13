"""generate command — AI-generated PR descriptions from git diff."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from prautopilot.core.config import AutopilotConfig
from prautopilot.core.diff import get_diff
from prautopilot.core.generator import generate_pr_description
from prautopilot.core.github import push_pr_description

generate_app = typer.Typer(help="Generate PR descriptions from your diff.")
console = Console()


@generate_app.callback(invoke_without_command=True)
def generate(
    ctx: typer.Context,
    base: str = typer.Option("main", "--base", "-b", help="Base branch to diff against"),
    industry: str = typer.Option("fintech", "--industry", "-i", help="Industry context"),
    push: bool = typer.Option(False, "--push/--no-push", help="Push description to open PR"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print without making changes"),
    max_lines: int = typer.Option(500, "--max-lines", help="Max diff lines to send to AI"),
) -> None:
    """Generate a PR description from your current branch diff.

    Examples:

        pr-autopilot generate

        pr-autopilot generate --base develop --industry manufacturing

        pr-autopilot generate --push
    """
    if ctx.invoked_subcommand is not None:
        return

    config = AutopilotConfig(
        industry=industry,
        base_branch=base,
        max_diff_lines=max_lines,
        push=push,
        dry_run=dry_run,
    )

    console.print(f"[dim]Diffing [cyan]{base}[/cyan]...HEAD[/dim]")

    diff = get_diff(base_branch=base)

    if diff.is_empty:
        console.print("[yellow]No changes detected against base branch.[/yellow]")
        raise typer.Exit(1)

    console.print(f"[dim]{diff.stat_line}[/dim]")
    console.print("[dim]Generating PR description...[/dim]")

    description = generate_pr_description(diff, config)

    console.print(Panel(
        Syntax(description, "markdown", theme="monokai", word_wrap=True),
        title=f"PR description — {diff.branch}",
        border_style="blue",
    ))

    if push and not dry_run:
        success = push_pr_description(description)
        if success:
            console.print("[green]✓ PR description updated on GitHub[/green]")
        else:
            console.print("[yellow]Could not push to GitHub — is there an open PR for this branch?[/yellow]")