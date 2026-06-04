# Initial Issue Backlog

These are the first issues to create on GitHub. They are kept here so the
project has a reproducible early roadmap even if issue text changes later.

## Add `maintainerkit.toml` support for custom triage rules

Labels: enhancement

Maintainers should be able to define their own keyword-to-label mappings,
priority rules, and route names without editing Python code.

Acceptance criteria:

- Load `maintainerkit.toml` from the current working directory or an explicit
  `--config` path.
- Merge project rules with the built-in defaults.
- Add tests for custom labels, priorities, and invalid configuration.
- Document a minimal config example in the README.

## Add a GitHub Actions scheduled triage example

Labels: documentation, good first issue

Small projects should be able to run MaintainerKit on a schedule and publish a
Markdown triage report as a workflow artifact.

Acceptance criteria:

- Add an example workflow under `examples/github-actions/`.
- Include comments explaining where issue or PR export happens.
- Document how to run the same command locally before enabling the workflow.

## Improve release notes with pull request references

Labels: enhancement

Release notes should preserve references such as `#123` and group them in a way
that maintainers can edit quickly before publishing.

Acceptance criteria:

- Detect issue and pull request references in commit subjects.
- Include references in Markdown output.
- Add tests for entries with one or more references.
- Keep unknown commit formats in the `Other` section.

## Add maintainer response templates

Labels: documentation, good first issue

Maintainers often repeat the same responses for missing reproductions,
oversized pull requests, security-sensitive reports, and unclear feature
requests.

Acceptance criteria:

- Add reusable Markdown templates under `docs/templates/`.
- Cover missing reproduction, large PR split request, security disclosure, and
  feature clarification.
- Link the templates from README or CONTRIBUTING.

## Add JSON schema documentation for triage input

Labels: documentation

The current README explains the input shape informally. A schema-style document
would make it easier for contributors to add exporters from GitHub, GitLab, or
other trackers.

Acceptance criteria:

- Document every supported triage input field.
- Mark required and optional fields.
- Include one issue example and one pull request example.
- Explain how unknown fields are handled.

