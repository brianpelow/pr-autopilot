"""Tests for label suggestion logic."""

from prautopilot.core.labels import suggest_labels
from prautopilot.core.diff import DiffSummary


def make_diff(files: list[str], content: str = "") -> DiffSummary:
    return DiffSummary(
        raw=content,
        files_changed=files,
        insertions=10,
        deletions=5,
        branch="feat/test",
        base_branch="main",
    )


def test_suggests_documentation_label() -> None:
    diff = make_diff(["README.md", "docs/guide.md"])
    labels = suggest_labels(diff)
    assert "documentation" in labels


def test_suggests_infrastructure_label() -> None:
    diff = make_diff(["docker-compose.yml", "terraform/main.tf"])
    labels = suggest_labels(diff)
    assert "infrastructure" in labels


def test_suggests_security_label() -> None:
    diff = make_diff(["auth/token.py"], content="+ secret_key = os.environ.get")
    labels = suggest_labels(diff)
    assert "security" in labels


def test_suggests_dependencies_label() -> None:
    diff = make_diff(["pyproject.toml", "uv.lock"])
    labels = suggest_labels(diff)
    assert "dependencies" in labels


def test_empty_diff_gets_enhancement() -> None:
    diff = make_diff(["some_random_file.py"])
    labels = suggest_labels(diff)
    assert "enhancement" in labels


def test_large_change_label() -> None:
    diff = DiffSummary(
        raw="x" * 100,
        files_changed=["big_file.py"],
        insertions=400,
        deletions=50,
        branch="feat/big",
        base_branch="main",
    )
    labels = suggest_labels(diff)
    assert "large-change" in labels