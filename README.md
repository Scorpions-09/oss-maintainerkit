# MaintainerKit

MaintainerKit is a small open-source toolkit for solo and small-team maintainers.
It turns issue lists, pull request metadata, and commit logs into practical
maintenance output: triage suggestions, review routing, release notes, and
repeatable checklists.

The project is intentionally local-first and dependency-light. It can run on a
maintainer's machine, in CI, or inside a scheduled workflow without sending
project data to a third-party service.

## Why this exists

Many useful open-source projects are maintained by one or two people. Those
maintainers often do not need a heavyweight governance platform; they need
boring, repeatable help with the work that piles up every week:

- label incoming issues and pull requests consistently
- identify security-sensitive reports early
- route large pull requests before review fatigue sets in
- generate release notes from commit history
- keep release, security, and onboarding routines visible

MaintainerKit focuses on those small maintenance loops first.

## Current MVP

- `triage`: reads issue or PR data from JSON and suggests labels, priority,
  routing, and the next maintainer action.
- `release`: reads commit subjects and generates grouped Markdown release notes.
- `checklist`: prints release, security, onboarding, or all checklists.

## Install

```bash
python -m pip install -e .
```

MaintainerKit supports Python 3.9 or newer and uses only the Python standard
library at runtime.

## Test

```bash
python -m unittest discover -s tests
```

## Quick start

Run triage on the included sample:

```bash
maintainerkit triage examples/items.json
```

Generate release notes:

```bash
maintainerkit release examples/commits.txt --version v0.1.0
```

Print maintenance checklists:

```bash
maintainerkit checklist --kind all
```

You can also run the package from source without installing the console script.
On PowerShell:

```bash
$env:PYTHONPATH = "src"; python -m maintainerkit triage examples/items.json
```

On macOS or Linux:

```bash
PYTHONPATH=src python -m maintainerkit triage examples/items.json
```

## Input format

The triage command expects a JSON array. Each item can be a simplified export or
a subset of GitHub API data.

```json
[
  {
    "number": 42,
    "type": "issue",
    "title": "Regression: login fails after v1.4.0",
    "body": "The login form returns a 500 error after upgrading.",
    "labels": ["bug"],
    "author": "contributor"
  }
]
```

Pull request items may include `changed_files`, `additions`, and `deletions` so
the tool can flag review risk.

## Example output

```text
### #42 Regression: login fails after v1.4.0

- Type: issue
- Priority: P1
- Suggested labels: bug, regression, needs-repro
- Route: maintainer triage
- Next action: Ask for a minimal reproduction, affected version, expected behavior, and actual behavior.
```

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md) for the current milestone plan.

Near-term work focuses on:

- GitHub Actions examples for scheduled triage reports.
- Configurable keyword rules through `maintainerkit.toml`.
- Maintainer-owned label taxonomies.
- Optional AI summarization for projects that choose to provide an API key.
- Markdown reports designed for issue comments and pull request reviews.

## Project values

- Maintainers stay in control of final decisions.
- Private project data should remain local by default.
- Small projects deserve good maintenance tools before they become large enough
  to attract platform-level automation.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, testing, and contribution
guidelines.
