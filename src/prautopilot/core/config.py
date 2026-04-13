"""Configuration models for pr-autopilot."""

from __future__ import annotations

import os
from pydantic import BaseModel, Field


class AutopilotConfig(BaseModel):
    """Runtime configuration for pr-autopilot."""

    industry: str = Field("fintech", description="Industry context for compliance notes")
    base_branch: str = Field("main", description="Base branch to diff against")
    max_diff_lines: int = Field(500, description="Max diff lines to send to AI")
    push: bool = Field(False, description="Push generated description to GitHub PR")
    dry_run: bool = Field(False, description="Print output without making changes")

    @classmethod
    def from_env(cls) -> "AutopilotConfig":
        return cls(
            industry=os.environ.get("PR_AUTOPILOT_INDUSTRY", "fintech"),
            base_branch=os.environ.get("PR_AUTOPILOT_BASE_BRANCH", "main"),
        )


COMPLIANCE_CONTEXT = {
    "fintech": (
        "This change is in a regulated financial services environment. "
        "Consider PCI-DSS scope, SOX change management requirements, "
        "FFIEC guidance, and audit trail implications."
    ),
    "manufacturing": (
        "This change is in a regulated manufacturing environment. "
        "Consider IEC 62443 security requirements, ISO 9001 change control, "
        "and traceability requirements."
    ),
    "regulated": (
        "This change is in a regulated environment. "
        "Consider SOC 2 change management, ISO 27001 controls, "
        "and audit trail requirements."
    ),
}