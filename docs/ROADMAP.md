# Roadmap

MaintainerKit is in its first public milestone. The goal is to prove that a
small local-first CLI can remove repetitive maintenance work for solo and
small-team open-source projects.

## Milestone 0.1: Useful Local CLI

Status: in progress

- Ship deterministic triage suggestions for issue and pull request JSON.
- Generate grouped release notes from commit subjects.
- Provide release, security, and onboarding checklists.
- Keep runtime dependencies at zero.
- Add examples that can be copied into small repositories.

## Milestone 0.2: Maintainer-Owned Rules

Status: planned

- Add `maintainerkit.toml` support for custom label rules.
- Let projects define priority rules without changing Python code.
- Support project-specific checklist extensions.
- Add validation errors that explain broken configuration clearly.

## Milestone 0.3: GitHub Workflow Integration

Status: planned

- Add a GitHub Actions example that runs a scheduled triage report.
- Document how to export issue and pull request data safely.
- Generate Markdown that can be pasted into issue comments.
- Add examples for dry-run reports in CI.

## Milestone 0.4: Optional AI Assistance

Status: planned

- Add opt-in issue summarization.
- Add opt-in release note polishing.
- Add opt-in contributor response drafts.
- Keep all networked behavior disabled unless the maintainer configures it.

## Non-Goals

- Replace maintainer judgment.
- Auto-close issues or pull requests by default.
- Require a hosted service.
- Send repository data to third parties without explicit maintainer consent.

