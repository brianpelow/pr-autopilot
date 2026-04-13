"""AI-powered PR description generation."""

from __future__ import annotations

import os
from prautopilot.core.diff import DiffSummary
from prautopilot.core.config import AutopilotConfig, COMPLIANCE_CONTEXT


PR_TEMPLATE = """## Summary

{summary}

## Type of change

{change_type}

## Key changes

{key_changes}

## Risk assessment

{risk}

## Testing

{testing}

## Compliance notes

{compliance}
"""


def generate_pr_description(diff: DiffSummary, config: AutopilotConfig) -> str:
    """Generate a PR description using the Anthropic API."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return _fallback_description(diff, config)

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        compliance_ctx = COMPLIANCE_CONTEXT.get(config.industry, COMPLIANCE_CONTEXT["regulated"])

        prompt = f"""You are a senior engineer reviewing a pull request in a {config.industry} engineering team.

Generate a structured PR description based on this git diff.

Branch: {diff.branch} -> {diff.base_branch}
Stats: {diff.stat_line}
Files changed: {", ".join(diff.files_changed[:10])}

Diff:
{diff.truncated(config.max_diff_lines)}

Compliance context: {compliance_ctx}

Generate a PR description with these exact sections:
## Summary
(2-3 sentences describing what changed and why)

## Type of change
(checkboxes: Bug fix / New feature / Refactor / Documentation / Infrastructure / Security)

## Key changes
(bullet points of the most important changes)

## Risk assessment
(blast radius, rollback complexity, data migrations, downstream impacts)

## Testing
(what was tested, what should reviewers verify)

## Compliance notes
(relevant regulatory considerations for {config.industry})

Be concise, technical, and specific to the actual diff. No generic filler."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    except Exception as e:
        return _fallback_description(diff, config)


def _fallback_description(diff: DiffSummary, config: AutopilotConfig) -> str:
    """Structured fallback when API is unavailable."""
    files = "\n".join(f"- {f}" for f in diff.files_changed[:10])
    compliance = COMPLIANCE_CONTEXT.get(config.industry, "")
    return PR_TEMPLATE.format(
        summary=f"Changes on branch `{diff.branch}`. {diff.stat_line}.",
        change_type="- [ ] Bug fix\n- [ ] New feature\n- [ ] Refactor\n- [ ] Documentation\n- [ ] Infrastructure",
        key_changes=files if files else "- See diff for details",
        risk="- Review carefully before merging",
        testing="- [ ] Tests added\n- [ ] Manually verified",
        compliance=compliance,
    )