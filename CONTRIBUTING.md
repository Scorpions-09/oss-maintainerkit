# Contributing

Thank you for helping improve MaintainerKit. This project is early, so small
focused contributions are especially valuable.

## Development setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .
```

On macOS or Linux, activate the environment with:

```bash
source .venv/bin/activate
```

## Run tests

```bash
python -m unittest discover -s tests
```

## Contribution guidelines

- Keep runtime dependencies optional unless they unlock a clear maintainer
  workflow.
- Prefer deterministic output so reports are easy to review in CI.
- Add tests for new triage rules, release-note grouping, and checklist changes.
- Avoid collecting or transmitting repository data by default.

## Good first contributions

- Add examples for other issue trackers.
- Improve keyword rules for documentation, security, and dependency work.
- Add checklist items for package ecosystems such as npm, PyPI, or crates.io.
