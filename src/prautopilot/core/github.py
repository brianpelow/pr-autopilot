"""GitHub API integration for pushing PR descriptions."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


def get_pr_number(repo_path: Path = Path(".")) -> int | None:
    """Get the PR number for the current branch using gh CLI."""
    result = subprocess.run(
        ["gh", "pr", "view", "--json", "number", "--jq", ".number"],
        cwd=repo_path, capture_output=True, text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return int(result.stdout.strip())
        except ValueError:
            return None
    return None


def push_pr_description(description: str, repo_path: Path = Path(".")) -> bool:
    """Push a PR description to the current branch PR using gh CLI."""
    pr_number = get_pr_number(repo_path)
    if pr_number is None:
        return False

    result = subprocess.run(
        ["gh", "pr", "edit", str(pr_number), "--body", description],
        cwd=repo_path, capture_output=True, text=True,
    )
    return result.returncode == 0


def push_pr_labels(labels: list[str], repo_path: Path = Path(".")) -> bool:
    """Add labels to the current branch PR."""
    pr_number = get_pr_number(repo_path)
    if pr_number is None:
        return False

    label_args = []
    for label in labels:
        label_args.extend(["--add-label", label])

    result = subprocess.run(
        ["gh", "pr", "edit", str(pr_number)] + label_args,
        cwd=repo_path, capture_output=True, text=True,
    )
    return result.returncode == 0