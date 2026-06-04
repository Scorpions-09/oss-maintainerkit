from __future__ import annotations

from collections.abc import Iterable


CHECKLISTS: dict[str, tuple[str, ...]] = {
    "release": (
        "Confirm tests pass on the supported Python versions.",
        "Review merged pull requests for breaking changes.",
        "Generate and edit release notes.",
        "Check dependency and security alerts.",
        "Tag the release and verify published artifacts.",
        "Open a follow-up issue for deferred maintenance work.",
    ),
    "security": (
        "Review security-labeled issues outside public discussion when needed.",
        "Check for leaked credentials in recent changes.",
        "Confirm dependency alerts have owners.",
        "Document supported versions and disclosure expectations.",
        "Record mitigation status before public release notes are published.",
    ),
    "onboarding": (
        "Verify README quick start works from a clean checkout.",
        "Keep contribution guidelines short and current.",
        "Label beginner-friendly issues with clear acceptance criteria.",
        "Explain project scope and non-goals.",
        "Respond to first-time contributors with the next concrete step.",
    ),
}


def available_checklists() -> tuple[str, ...]:
    return tuple(CHECKLISTS)


def render_checklist(kind: str) -> str:
    if kind == "all":
        return "\n\n".join(render_checklist(name) for name in CHECKLISTS)
    if kind not in CHECKLISTS:
        valid = ", ".join((*CHECKLISTS.keys(), "all"))
        raise ValueError(f"Unknown checklist kind {kind!r}. Expected one of: {valid}.")

    title = kind.replace("-", " ").title()
    items = "\n".join(f"- [ ] {item}" for item in CHECKLISTS[kind])
    return f"## {title} Checklist\n\n{items}"


def render_custom_checklist(title: str, items: Iterable[str]) -> str:
    body = "\n".join(f"- [ ] {item}" for item in items)
    return f"## {title}\n\n{body}"

