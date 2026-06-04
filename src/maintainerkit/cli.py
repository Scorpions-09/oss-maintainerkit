from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .checklists import available_checklists, render_checklist
from .release_notes import build_release_json, build_release_notes, parse_commit_lines
from .triage import analyze_items, load_items_json, render_json, render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="maintainerkit",
        description="Local-first automation helpers for small open-source maintainers.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    triage = subparsers.add_parser("triage", help="Suggest labels, priority, route, and next action.")
    triage.add_argument("input", help="Path to a JSON array of issues or pull requests.")
    triage.add_argument("--format", choices=("markdown", "json"), default="markdown")
    triage.add_argument("--output", help="Optional output path.")

    release = subparsers.add_parser("release", help="Generate release notes from commit subjects.")
    release.add_argument("input", help="Path to a text file with one commit subject per line.")
    release.add_argument("--version", help="Release version, for example v0.1.0.")
    release.add_argument("--format", choices=("markdown", "json"), default="markdown")
    release.add_argument("--output", help="Optional output path.")

    checklist = subparsers.add_parser("checklist", help="Print maintainer checklists.")
    checklist.add_argument(
        "--kind",
        choices=(*available_checklists(), "all"),
        default="release",
        help="Checklist to print.",
    )
    checklist.add_argument("--output", help="Optional output path.")

    return parser


def write_output(content: str, output: str | None) -> None:
    if output:
        Path(output).write_text(content, encoding="utf-8")
    else:
        sys.stdout.write(content)


def run_triage(args: argparse.Namespace) -> int:
    items = load_items_json(args.input)
    results = analyze_items(items)
    content = render_json(results) if args.format == "json" else render_markdown(results)
    write_output(content, args.output)
    return 0


def run_release(args: argparse.Namespace) -> int:
    lines = Path(args.input).read_text(encoding="utf-8").splitlines()
    entries = parse_commit_lines(lines)
    content = (
        build_release_json(entries, args.version)
        if args.format == "json"
        else build_release_notes(entries, args.version)
    )
    write_output(content, args.output)
    return 0


def run_checklist(args: argparse.Namespace) -> int:
    write_output(render_checklist(args.kind) + "\n", args.output)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "triage":
            return run_triage(args)
        if args.command == "release":
            return run_release(args)
        if args.command == "checklist":
            return run_checklist(args)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"maintainerkit: error: {exc}\n")

    parser.error(f"Unknown command: {args.command}")
    return 2

