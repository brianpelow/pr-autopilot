"""Tests for DiffSummary."""

from prautopilot.core.diff import DiffSummary


def test_diff_summary_is_empty() -> None:
    diff = DiffSummary(raw="", files_changed=[], insertions=0, deletions=0, branch="main", base_branch="main")
    assert diff.is_empty is True


def test_diff_summary_not_empty() -> None:
    diff = DiffSummary(raw="+ some change", files_changed=["file.py"], insertions=1, deletions=0, branch="feat/x", base_branch="main")
    assert diff.is_empty is False


def test_diff_stat_line() -> None:
    diff = DiffSummary(raw="x", files_changed=["a.py", "b.py"], insertions=10, deletions=3, branch="feat/x", base_branch="main")
    assert "2 file(s)" in diff.stat_line
    assert "+10" in diff.stat_line
    assert "-3" in diff.stat_line


def test_diff_truncation() -> None:
    lines = [f"line {i}" for i in range(600)]
    diff = DiffSummary(raw="\n".join(lines), files_changed=[], insertions=0, deletions=0, branch="x", base_branch="main")
    truncated = diff.truncated(max_lines=100)
    assert "truncated" in truncated
    assert len(truncated.splitlines()) <= 102