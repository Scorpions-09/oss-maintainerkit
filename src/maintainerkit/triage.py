from __future__ import annotations

from dataclasses import dataclass, field
import json
import re
from typing import Any, Iterable


KEYWORD_LABELS: dict[str, tuple[str, ...]] = {
    "security": (
        "auth bypass",
        "cve",
        "credential",
        "exploit",
        "injection",
        "private key",
        "secret",
        "token leak",
        "vulnerability",
        "xss",
    ),
    "bug": (
        "bug",
        "broken",
        "crash",
        "error",
        "exception",
        "fail",
        "fails",
        "failure",
        "traceback",
    ),
    "regression": ("regression", "worked before", "after upgrading", "since v"),
    "docs": ("docs", "documentation", "example", "readme", "typo"),
    "enhancement": ("feature", "proposal", "request", "support", "would like"),
    "ci": ("ci", "github actions", "workflow", "build failed", "build failing"),
    "dependencies": ("dependency", "dependencies", "dependabot", "npm audit", "pip audit"),
    "performance": ("latency", "memory leak", "performance", "slow", "timeout"),
    "tests": ("coverage", "flaky", "test", "tests"),
}

REPRODUCTION_HINTS = (
    "steps to reproduce",
    "reproduction",
    "minimal repro",
    "expected",
    "actual",
    "version",
)


@dataclass(frozen=True)
class WorkItem:
    title: str
    body: str = ""
    item_type: str = "issue"
    number: int | str | None = None
    labels: tuple[str, ...] = ()
    author: str | None = None
    changed_files: int = 0
    additions: int = 0
    deletions: int = 0
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "WorkItem":
        item_type = str(data.get("type") or data.get("item_type") or "").lower()
        if not item_type:
            item_type = "pr" if data.get("pull_request") else "issue"

        labels = data.get("labels") or ()
        if labels and isinstance(labels[0], dict):
            labels = tuple(str(label.get("name", "")) for label in labels if label.get("name"))
        else:
            labels = tuple(str(label) for label in labels)

        user = data.get("user") or {}

        return cls(
            title=str(data.get("title", "")).strip(),
            body=str(data.get("body", "") or "").strip(),
            item_type=normalize_item_type(item_type),
            number=data.get("number"),
            labels=labels,
            author=data.get("author") or user.get("login"),
            changed_files=int(data.get("changed_files") or 0),
            additions=int(data.get("additions") or 0),
            deletions=int(data.get("deletions") or 0),
            raw=data,
        )


@dataclass(frozen=True)
class TriageResult:
    item: WorkItem
    suggested_labels: tuple[str, ...]
    priority: str
    route: str
    next_action: str
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "number": self.item.number,
            "title": self.item.title,
            "type": self.item.item_type,
            "priority": self.priority,
            "suggested_labels": list(self.suggested_labels),
            "route": self.route,
            "next_action": self.next_action,
            "reasons": list(self.reasons),
        }


def normalize_item_type(value: str) -> str:
    normalized = value.lower().strip()
    if normalized in {"pull_request", "pull-request", "pr"}:
        return "pr"
    return "issue"


def analyze_text(title: str, body: str) -> tuple[set[str], list[str]]:
    text = f"{title}\n{body}".lower()
    labels: set[str] = set()
    reasons: list[str] = []

    for label, keywords in KEYWORD_LABELS.items():
        for keyword in keywords:
            if keyword_matches(text, keyword):
                labels.add(label)
                reasons.append(f"Matched {label!r} keyword: {keyword}")
                break

    return labels, reasons


def keyword_matches(text: str, keyword: str) -> bool:
    if " " in keyword:
        return keyword in text
    return re.search(rf"\b{re.escape(keyword)}\b", text) is not None


def has_reproduction(body: str) -> bool:
    lowered = body.lower()
    matches = sum(1 for hint in REPRODUCTION_HINTS if hint in lowered)
    return matches >= 2


def is_large_pr(item: WorkItem) -> bool:
    total_changes = item.additions + item.deletions
    return item.item_type == "pr" and (item.changed_files >= 12 or total_changes >= 500)


def priority_for(labels: set[str], item: WorkItem) -> str:
    if "security" in labels:
        return "P0"
    if "regression" in labels:
        return "P1"
    if "bug" in labels and re.search(r"\b(crash|data loss|traceback|exception)\b", item.body.lower()):
        return "P1"
    if is_large_pr(item):
        return "P2"
    if "bug" in labels or "ci" in labels:
        return "P2"
    return "P3"


def route_for(labels: set[str], item: WorkItem) -> str:
    if "security" in labels:
        return "security review"
    if item.item_type == "pr" and is_large_pr(item):
        return "maintainer review planning"
    if "dependencies" in labels:
        return "dependency maintenance"
    if "docs" in labels:
        return "documentation"
    if "ci" in labels:
        return "build and release"
    if "enhancement" in labels:
        return "product discussion"
    return "maintainer triage"


def next_action_for(labels: set[str], item: WorkItem) -> str:
    if "security" in labels:
        return (
            "Move discussion to the private security process, confirm impact, "
            "and avoid exposing exploit details publicly."
        )
    if "regression" in labels:
        return "Confirm the last known good version, first affected version, and assign an owner."
    if item.item_type == "pr" and is_large_pr(item):
        return "Ask whether the pull request can be split or reviewed in smaller commits."
    if item.item_type == "issue" and "bug" in labels and not has_reproduction(item.body):
        return "Ask for a minimal reproduction, affected version, expected behavior, and actual behavior."
    if "enhancement" in labels:
        return "Ask for the user story, constraints, and a small acceptance test."
    if "docs" in labels:
        return "Check whether the docs change needs examples, screenshots, or migration notes."
    if item.item_type == "pr":
        return "Run tests, scan the diff size, and assign the most relevant reviewer."
    return "Confirm scope, add labels, and decide whether this needs an owner or a discussion."


def analyze_item(item: WorkItem) -> TriageResult:
    labels, reasons = analyze_text(item.title, item.body)
    labels.update(label.lower() for label in item.labels)

    if item.item_type == "issue" and "bug" in labels and not has_reproduction(item.body):
        labels.add("needs-repro")
        reasons.append("Bug report is missing enough reproduction details.")

    if is_large_pr(item):
        labels.add("needs-split")
        reasons.append("Pull request is large enough to need review planning.")

    priority = priority_for(labels, item)
    route = route_for(labels, item)
    next_action = next_action_for(labels, item)

    return TriageResult(
        item=item,
        suggested_labels=tuple(sorted(labels)),
        priority=priority,
        route=route,
        next_action=next_action,
        reasons=tuple(reasons),
    )


def analyze_items(items: Iterable[WorkItem]) -> list[TriageResult]:
    return [analyze_item(item) for item in items]


def load_items_json(path: str) -> list[WorkItem]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if isinstance(payload, dict) and "items" in payload:
        payload = payload["items"]
    if not isinstance(payload, list):
        raise ValueError("Triage input must be a JSON array or an object with an 'items' array.")

    return [WorkItem.from_mapping(item) for item in payload]


def render_markdown(results: Iterable[TriageResult]) -> str:
    lines: list[str] = ["# Maintainer Triage Report", ""]
    for result in results:
        number = f"#{result.item.number} " if result.item.number is not None else ""
        labels = ", ".join(result.suggested_labels) or "none"
        lines.extend(
            [
                f"### {number}{result.item.title}",
                "",
                f"- Type: {result.item.item_type}",
                f"- Priority: {result.priority}",
                f"- Suggested labels: {labels}",
                f"- Route: {result.route}",
                f"- Next action: {result.next_action}",
            ]
        )
        if result.reasons:
            lines.append(f"- Reason: {'; '.join(result.reasons)}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_json(results: Iterable[TriageResult]) -> str:
    return json.dumps([result.to_dict() for result in results], indent=2)
