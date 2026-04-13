# pr-autopilot

> CLI that auto-generates PR descriptions, reviewers, and labels from your diff using AI.

![CI](https://github.com/brianpelow/pr-autopilot/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)

## Overview

`pr-autopilot` eliminates the friction of writing pull request descriptions.
It reads your git diff, understands the change, and generates a structured PR
description using Claude. Built for engineering teams in regulated financial
services, fintech, and manufacturing where clear change documentation is a
compliance requirement, not just good practice.

Run it standalone, pipe it into your CI pipeline, or install it as a git hook
so every PR is documented before it is opened.

## Quick start

```bash
pip install pr-autopilot

# Generate a PR description from your current branch diff
pr-autopilot generate

# Generate and push directly to an open GitHub PR
pr-autopilot generate --push

# Suggest reviewers based on changed files
pr-autopilot review

# Auto-label the PR by change type
pr-autopilot label

# Install as a git hook (runs automatically on every push)
pr-autopilot hook install
```

## Commands

| Command | Description |
|---------|-------------|
| `pr-autopilot generate` | Generate PR description from current diff |
| `pr-autopilot review` | Suggest reviewers based on changed files |
| `pr-autopilot label` | Suggest labels based on change type |
| `pr-autopilot hook install` | Install as git prepare-commit-msg hook |
| `pr-autopilot hook uninstall` | Remove the git hook |

## Generated PR format

```markdown
## Summary
Brief description of what changed and why.

## Type of change
- [x] Feature / Bug fix / Refactor / Docs / Infrastructure

## Key changes
- List of meaningful changes extracted from the diff

## Risk assessment
- Blast radius, rollback complexity, data migrations

## Testing
- What was tested and how

## Compliance notes
- Relevant regulatory considerations (fintech/manufacturing context)
```

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Claude API key for generation | Yes |
| `GITHUB_TOKEN` | GitHub token for pushing descriptions | No |
| `PR_AUTOPILOT_INDUSTRY` | Industry context (fintech/manufacturing) | No |

## Industry context

In regulated environments, PR descriptions serve as audit trail artifacts.
`pr-autopilot` generates descriptions that include risk assessment and
compliance notes relevant to fintech (PCI-DSS, SOX) and manufacturing
(IEC 62443, ISO 9001) contexts.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0 — see [LICENSE](LICENSE).