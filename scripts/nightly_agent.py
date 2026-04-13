"""Nightly agent — automated maintenance for pr-autopilot."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

REPO_ROOT = Path(__file__).parent.parent


def update_label_stats() -> None:
    """Write a summary of all label rules to docs."""
    from prautopilot.core.labels import LABEL_RULES
    stats = {
        "generated_at": datetime.utcnow().isoformat(),
        "date": date.today().isoformat(),
        "label_count": len(LABEL_RULES),
        "labels": [{"label": label, "keyword_count": len(kws)} for label, kws in LABEL_RULES],
    }
    out = REPO_ROOT / "docs" / "label-stats.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(stats, indent=2))
    print(f"[agent] Updated label stats -> {out}")


def refresh_changelog() -> None:
    changelog = REPO_ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return
    today = date.today().isoformat()
    content = changelog.read_text()
    if today not in content:
        content = content.replace("## [Unreleased]", f"## [Unreleased]\n\n_Last checked: {today}_", 1)
        changelog.write_text(content)
    print("[agent] Refreshed CHANGELOG timestamp")


if __name__ == "__main__":
    print(f"[agent] Starting nightly agent - {date.today().isoformat()}")
    update_label_stats()
    refresh_changelog()
    print("[agent] Done.")