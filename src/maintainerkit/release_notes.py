from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import json
import re
from typing import Iterable


COMMIT_RE = re.compile(
    r"^(?:(?P<hash>[0-9a-f]{7,40})\s+)?"
    r"(?P<kind>[a-zA-Z]+)"
    r"(?:\((?P<scope>[^)]+)\))?"
    r"(?P<breaking>!)?:\s+"
    r"(?P<description>.+)$"
)


SECTION_TITLES = {
    "feat": "Added",
    "fix": "Fixed",
    "perf": "Performance",
    "docs": "Documentation",
    "refactor": "Changed",
    "test": "Tests",
    "chore": "Maintenance",
    "build": "Build",
    "ci": "CI",
    "deps": "Dependencies",
    "security": "Security",
}


@dataclass(frozen=True)
class CommitEntry:
    kind: str
    description: str
    scope: str | None = None
    breaking: bool = False
    raw: str = ""

    @property
    def section(self) -> str:
        return SECTION_TITLES.get(self.kind, "Other")

    def to_markdown_item(self) -> str:
        prefix = f"**{self.scope}:** " if self.scope else ""
        suffix = " **BREAKING**" if self.breaking else ""
        return f"- {prefix}{self.description}{suffix}"

    def to_dict(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "scope": self.scope,
            "description": self.description,
            "breaking": self.breaking,
            "section": self.section,
            "raw": self.raw,
        }


def parse_commit_line(line: str) -> CommitEntry | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    match = COMMIT_RE.match(stripped)
    if not match:
        return CommitEntry(kind="other", description=stripped, raw=stripped)

    kind = match.group("kind").lower()
    return CommitEntry(
        kind=kind,
        scope=match.group("scope"),
        description=match.group("description").strip(),
        breaking=bool(match.group("breaking")),
        raw=stripped,
    )


def parse_commit_lines(lines: Iterable[str]) -> list[CommitEntry]:
    entries: list[CommitEntry] = []
    for line in lines:
        entry = parse_commit_line(line)
        if entry is not None:
            entries.append(entry)
    return entries


def group_entries(entries: Iterable[CommitEntry]) -> dict[str, list[CommitEntry]]:
    grouped: dict[str, list[CommitEntry]] = {}
    for entry in entries:
        grouped.setdefault(entry.section, []).append(entry)
    return grouped


def build_release_notes(entries: Iterable[CommitEntry], version: str | None = None) -> str:
    entry_list = list(entries)
    title = version or "Unreleased"
    lines = [f"# {title}", "", f"Released: {date.today().isoformat()}", ""]

    breaking_entries = [entry for entry in entry_list if entry.breaking]
    if breaking_entries:
        lines.extend(["## Breaking Changes", ""])
        lines.extend(entry.to_markdown_item() for entry in breaking_entries)
        lines.append("")

    grouped = group_entries(entry_list)
    ordered_sections = [
        "Security",
        "Added",
        "Fixed",
        "Performance",
        "Changed",
        "Documentation",
        "Dependencies",
        "Tests",
        "Build",
        "CI",
        "Maintenance",
        "Other",
    ]

    for section in ordered_sections:
        section_entries = grouped.get(section)
        if not section_entries:
            continue
        section_entries = [entry for entry in section_entries if not entry.breaking]
        if not section_entries:
            continue
        lines.extend([f"## {section}", ""])
        lines.extend(entry.to_markdown_item() for entry in section_entries)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_release_json(entries: Iterable[CommitEntry], version: str | None = None) -> str:
    entry_list = list(entries)
    payload = {
        "version": version or "Unreleased",
        "released": date.today().isoformat(),
        "entries": [entry.to_dict() for entry in entry_list],
    }
    return json.dumps(payload, indent=2)
