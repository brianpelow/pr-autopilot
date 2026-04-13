"""PR label classification logic."""

from __future__ import annotations

from prautopilot.core.diff import DiffSummary

LABEL_RULES: list[tuple[str, list[str]]] = [
    ("breaking-change", ["BREAKING", "breaking change", "incompatible"]),
    ("security", ["auth", "crypt", "secret", "token", "permission", "vulnerability", "CVE"]),
    ("infrastructure", ["dockerfile", "docker-compose", "terraform", ".yml", ".yaml", "kubernetes", "helm"]),
    ("dependencies", ["requirements", "pyproject", "package.json", "uv.lock", "poetry.lock"]),
    ("documentation", [".md", ".rst", "docs/", "README"]),
    ("testing", ["test_", "_test", "spec.", ".test.", "conftest"]),
    ("database", ["migration", "schema", "alembic", "flyway", "sql"]),
    ("compliance", ["audit", "compliance", "regulatory", "pci", "sox", "gdpr"]),
]


def suggest_labels(diff: DiffSummary) -> list[str]:
    """Suggest GitHub labels based on changed files and diff content."""
    labels: set[str] = set()
    content = diff.raw.lower() + "\n".join(diff.files_changed).lower()

    for label, keywords in LABEL_RULES:
        if any(kw.lower() in content for kw in keywords):
            labels.add(label)

    if diff.insertions > 300:
        labels.add("large-change")

    if not labels:
        labels.add("enhancement")

    return sorted(labels)