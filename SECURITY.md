# Security Policy

`agent-run-report` reads local Git metadata and an optional local agent log file to generate Markdown and JSON reports.

The tool does not execute coding-agent commands, does not run shell commands from log files, and does not upload data. It only invokes local `git` commands against the repository path supplied by the user.

Users should not include secrets in agent logs. Logs can contain credentials, private file paths, terminal output, proprietary source snippets, or other sensitive data. Generated reports may also contain sensitive file paths, diff statistics, log excerpts, traceback text, and optional diff snippets.

Review generated reports before publishing them in a GitHub issue, pull request, chat, ticket, or other shared location.

The `--redact` option masks common token-like patterns in report text fields, but it is not a complete secret scanner. It can miss credentials and can redact harmless text. If a real credential appears in a log or report, rotate it.

To report a vulnerability, open a private security advisory on GitHub if available, or contact the maintainers through the repository issue tracker without posting sensitive details publicly.
