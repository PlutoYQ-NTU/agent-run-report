# Privacy And Redaction

Reports can include local paths, Git status, log excerpts, traceback text, and optional diff excerpts. Review reports before sharing them publicly.

## Redaction Option

Use `--redact` to mask common token-like strings in report text fields:

```bash
agent-run-report \
  --repo . \
  --log logs/latest.txt \
  --out reports/run_report.md \
  --json-out reports/run_report.json \
  --redact
```

The redactor looks for common patterns such as:

- `sk-...` style API keys
- `AKIA...` style access key identifiers
- `ghp_...` and related GitHub token prefixes
- `xox...` style Slack token prefixes
- bearer tokens
- simple `api_key=...`, `token=...`, `secret=...`, and `password=...` assignments

## Limitations

Redaction is best-effort and pattern-based. It can miss secrets and can redact harmless text. It does not inspect binary files, upload reports, or rewrite source files.

Avoid including secrets in logs. If a secret appears in a report, rotate that credential according to the provider's guidance.
