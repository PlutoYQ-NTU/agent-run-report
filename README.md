# agent-run-report

[![tests](https://github.com/PlutoYQ-NTU/agent-run-report/actions/workflows/tests.yml/badge.svg)](https://github.com/PlutoYQ-NTU/agent-run-report/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

`agent-run-report` is a lightweight Python CLI that turns a local coding-agent run into a clean Markdown and optional JSON report.

It summarizes Git repository status, changed files, diff statistics, optional diff excerpts, agent log findings, detected errors and warnings, test output hints, suggested next steps, and a PR or issue comment-ready update.

## Why this exists

Long-running coding-agent sessions can leave maintainers with scattered terminal output, partial logs, changed files, and unclear next steps. This tool creates a single report that is easy to review locally or paste into a GitHub pull request, issue, handoff note, or maintenance record.

It is designed for runs from tools such as Codex CLI, Claude Code, Cline, and other local coding agents.

## Installation

From a local checkout:

```bash
pip install -e .
```

For development, install pytest separately or with the optional development extra:

```bash
pip install -e ".[dev]"
```

## Quick start

Generate a Markdown report for the current repository:

```bash
agent-run-report --repo . --log logs/latest.txt --out reports/run_report.md
```

Generate Markdown and JSON:

```bash
agent-run-report --repo . --log logs/latest.txt --out reports/run_report.md --json-out reports/run_report.json
```

Include a bounded diff excerpt:

```bash
agent-run-report --repo . --log logs/latest.txt --out reports/run_report.md --include-diff --max-diff-lines 200
```

Build a report summary without writing files:

```bash
agent-run-report --repo . --log logs/latest.txt --dry-run
```

Redact common token-like strings from report fields:

```bash
agent-run-report --repo . --log logs/latest.txt --out reports/run_report.md --redact
```

## CLI options

```text
--repo PATH            Repository path. Default: current directory.
--log PATH             Optional agent log file.
--out PATH             Markdown report output path. Default: reports/run_report.md.
--json-out PATH        Optional JSON report output path.
--include-diff         Include a diff excerpt in the Markdown and JSON data.
--max-diff-lines INT   Max lines of full diff excerpt. Default: 200.
--title TEXT           Optional report title. Default: Agent Run Report.
--no-next-steps        Disable automatic next-step suggestions.
--redact               Redact common token-like strings from report text fields.
--dry-run              Build the report and print a summary without writing files.
```

## Example output

```markdown
# Agent Run Report

## Summary

Repository has 3 changed file(s). 1 error line and 1 warning line were detected in the provided log.

## Repository

- Path: `/work/project`
- Branch: `main`
- Commit: `abc1234`

## Suggested Next Steps

- Fix detected errors before handing off or opening a PR.
- Rerun the failing test command after fixes.
```

See `examples/sample_report.md` and `examples/sample_report.json` for complete examples.

See `docs/report_schema.md` for JSON field documentation and `docs/privacy_redaction.md` for privacy and redaction guidance.

## Use cases

- Codex CLI long-running job report.
- Claude Code or Cline run summary.
- GitHub issue or PR update.
- Local maintenance automation.

## Limitations

- Log parsing is rule-based and intentionally conservative.
- Test detection is based on text hints, not framework APIs.
- Diff excerpts may contain sensitive source code if enabled.
- Redaction is best-effort and can miss secrets.
- The tool expects `git` to be available on `PATH`.
- It does not upload, redact, or publish reports automatically.

## Roadmap

Planned ideas include GitHub PR comment mode, multiple log inputs, HTML output, richer test framework detection, integration with agent approval tools, and GitHub Actions support.

## Related projects

This repository is part of a small toolkit for local coding-agent workflows and small local LLM evaluation:

- [`agent-approval-gate`](https://github.com/PlutoYQ-NTU/agent-approval-gate): classify command risk before a local coding agent runs shell commands.
- [`agent-run-report`](https://github.com/PlutoYQ-NTU/agent-run-report): generate Markdown and JSON reports after a local coding-agent run.
- [`mini-llm-eval-kit`](https://github.com/PlutoYQ-NTU/mini-llm-eval-kit): evaluate small local language models with configurable prompt suites.
## Contributing

Issues and pull requests are welcome. Keep the project small, dependency-light, and useful for local maintainer workflows. Please add tests for parser or report-formatting changes.
