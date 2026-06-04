# Report Schema

`agent-run-report` writes Markdown for humans and optional JSON for automation. The JSON report is intentionally flat and stable enough for lightweight scripts.

## Top-Level Fields

```json
{
  "title": "Agent Run Report",
  "repo_path": "/work/project",
  "branch": "main",
  "commit": "abc1234",
  "status_short": " M src/app.py",
  "changed_files": ["src/app.py"],
  "diff_stat": "src/app.py | 2 ++",
  "log_path": "/work/project/logs/latest.txt",
  "log_excerpt": "...",
  "errors": [],
  "warnings": [],
  "tracebacks": [],
  "test_summary": "1 passed",
  "failed_command_hints": [],
  "suggested_next_steps": [],
  "diff_excerpt": ""
}
```

## Field Notes

- `status_short` is the raw `git status --short` output.
- `changed_files` is parsed from `status_short`; renamed files use the new path.
- `diff_stat` comes from `git diff --stat` when available.
- `diff_excerpt` is included only when `--include-diff` is used.
- `log_excerpt` is a bounded excerpt of the provided log.
- `errors`, `warnings`, `tracebacks`, `test_summary`, and `failed_command_hints` are rule-based hints from log text.
- `suggested_next_steps` is generated from simple heuristics unless `--no-next-steps` is used.

## Compatibility

The schema may grow in minor releases. Consumers should ignore unknown fields and avoid relying on Markdown formatting for automation.
