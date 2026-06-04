# Contributing

`agent-run-report` should stay small, local-first, and dependency-light.

## Development

```bash
pip install -e ".[dev]"
python -m pytest
```

## Parser And Report Changes

When changing parser or report behavior:

- Add tests for log parsing, changed-file parsing, Markdown or JSON output, and CLI behavior.
- Update `docs/report_schema.md` for JSON field changes.
- Update `docs/privacy_redaction.md` for redaction behavior changes.
- Avoid automatic uploads or network publishing.

## Privacy

Do not add examples that include real tokens, private logs, private paths that identify a person, or proprietary code excerpts.
