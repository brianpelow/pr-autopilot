"""Tests for AutopilotConfig."""

from prautopilot.core.config import AutopilotConfig, COMPLIANCE_CONTEXT


def test_config_defaults() -> None:
    config = AutopilotConfig()
    assert config.industry == "fintech"
    assert config.base_branch == "main"
    assert config.max_diff_lines == 500
    assert config.push is False
    assert config.dry_run is False


def test_config_custom() -> None:
    config = AutopilotConfig(industry="manufacturing", base_branch="develop")
    assert config.industry == "manufacturing"
    assert config.base_branch == "develop"


def test_compliance_context_fintech() -> None:
    assert "fintech" in COMPLIANCE_CONTEXT
    assert "PCI-DSS" in COMPLIANCE_CONTEXT["fintech"]


def test_compliance_context_manufacturing() -> None:
    assert "manufacturing" in COMPLIANCE_CONTEXT
    assert "IEC 62443" in COMPLIANCE_CONTEXT["manufacturing"]