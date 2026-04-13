"""Git diff extraction and processing."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DiffSummary:
    """Processed summary of a git diff."""

    raw: str
    files_changed: list[str]
    insertions: int
    deletions: int
    branch: str
    base_branch: str

    @property
    def is_empty(self) -> bool:
        return not self.raw.strip()

    @property
    def stat_line(self) -> str:
        return (
            f"{len(self.files_changed)} file(s) changed, "
            f"+{self.insertions} insertions, -{self.deletions} deletions"
        )

    def truncated(self, max_lines: int = 500) -> str:
        lines = self.raw.splitlines()
        if len(lines) <= max_lines:
            return self.raw
        kept = lines[:max_lines]
        kept.append(f"\n... diff truncated at {max_lines} lines ({len(lines) - max_lines} more) ...")
        return "\n".join(kept)


def get_current_branch(repo_path: Path = Path(".")) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo_path, capture_output=True, text=True, check=True,
    )
    return result.stdout.strip()


def get_diff(base_branch: str = "main", repo_path: Path = Path(".")) -> DiffSummary:
    """Extract the diff between current branch and base branch."""
    branch = get_current_branch(repo_path)

    diff_result = subprocess.run(
        ["git", "diff", f"{base_branch}...HEAD"],
        cwd=repo_path, capture_output=True, text=True,
    )
    raw_diff = diff_result.stdout

    stat_result = subprocess.run(
        ["git", "diff", "--stat", f"{base_branch}...HEAD"],
        cwd=repo_path, capture_output=True, text=True,
    )
    stat_output = stat_result.stdout

    files_changed: list[str] = []
    insertions = 0
    deletions = 0

    for line in stat_output.splitlines():
        if "|" in line:
            parts = line.split("|")
            if len(parts) >= 1:
                files_changed.append(parts[0].strip())
        if "insertion" in line or "deletion" in line:
            tokens = line.split()
            for i, token in enumerate(tokens):
                if "insertion" in token and i > 0:
                    try:
                        insertions = int(tokens[i - 1])
                    except ValueError:
                        pass
                if "deletion" in token and i > 0:
                    try:
                        deletions = int(tokens[i - 1])
                    except ValueError:
                        pass

    return DiffSummary(
        raw=raw_diff,
        files_changed=files_changed,
        insertions=insertions,
        deletions=deletions,
        branch=branch,
        base_branch=base_branch,
    )