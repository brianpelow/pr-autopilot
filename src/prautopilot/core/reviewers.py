"""Reviewer suggestion logic based on changed files."""

from __future__ import annotations

import subprocess
from pathlib import Path

from prautopilot.core.diff import DiffSummary


def suggest_reviewers(diff: DiffSummary, repo_path: Path = Path("."), top_n: int = 3) -> list[str]:
    """Suggest reviewers by finding who last touched the changed files."""
    reviewer_scores: dict[str, int] = {}

    for file_path in diff.files_changed[:20]:
        result = subprocess.run(
            ["git", "log", "--follow", "--format=%ae", "-n", "5", "--", file_path],
            cwd=repo_path, capture_output=True, text=True,
        )
        for email in result.stdout.strip().splitlines():
            email = email.strip()
            if email:
                reviewer_scores[email] = reviewer_scores.get(email, 0) + 1

    current = subprocess.run(
        ["git", "config", "user.email"],
        cwd=repo_path, capture_output=True, text=True,
    ).stdout.strip()

    sorted_reviewers = sorted(reviewer_scores.items(), key=lambda x: x[1], reverse=True)
    return [email for email, _ in sorted_reviewers if email != current][:top_n]