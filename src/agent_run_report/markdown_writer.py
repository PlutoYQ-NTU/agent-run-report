"""Markdown rendering for agent run reports."""

from __future__ import annotations

from .report_model import Report


def render_markdown(report: Report) -> str:
    """Render a complete Markdown report."""
    sections = [
        f"# {report.title}",
        "",
        "## Summary",
        "",
        _summary(report),
        "",
        "## Repository",
        "",
        f"- Path: `{report.repo_path}`",
        f"- Branch: `{report.branch}`",
        f"- Commit: `{report.commit}`",
        "",
        "## Changed Files",
        "",
        _bullet_list(report.changed_files, "No changed files detected."),
        "",
        "## Diff Stat",
        "",
        _code_or_note(report.diff_stat, "No diff statistics detected."),
        "",
        "## Log Findings",
        "",
        _log_findings(report),
        "",
        "## Errors",
        "",
        _bullet_list(report.errors, "No errors detected in the provided log."),
        "",
        "## Warnings",
        "",
        _bullet_list(report.warnings, "No warnings detected in the provided log."),
        "",
        "## Test Summary",
        "",
        report.test_summary or "No test summary detected in the provided log.",
        "",
        "## Diff Excerpt",
        "",
        _code_or_note(report.diff_excerpt, "No diff excerpt included."),
        "",
        "## Suggested Next Steps",
        "",
        _bullet_list(report.suggested_next_steps, "Automatic next-step suggestions were disabled."),
        "",
        "## PR / Issue Comment",
        "",
        _pr_comment(report),
        "",
    ]
    return "\n".join(sections)


def write_markdown(report: Report, path: str) -> None:
    """Write a Markdown report to path."""
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(render_markdown(report))


def _summary(report: Report) -> str:
    pieces: list[str] = []
    changed_count = len(report.changed_files)
    pieces.append(f"Repository has {changed_count} changed file(s).")

    if report.log_path:
        pieces.append(f"Log parsed from `{report.log_path}`.")
    else:
        pieces.append("No log file was provided.")

    pieces.append(f"Detected {len(report.errors)} error line(s) and {len(report.warnings)} warning line(s).")
    if report.test_summary:
        pieces.append(f"Latest test summary hint: {report.test_summary}")
    return " ".join(pieces)


def _log_findings(report: Report) -> str:
    lines = [
        f"- Log path: `{report.log_path}`" if report.log_path else "- Log path: Not provided.",
        f"- Traceback blocks: {len(report.tracebacks)}",
        f"- Failed command hints: {len(report.failed_command_hints)}",
    ]
    if report.failed_command_hints:
        lines.append("")
        lines.append("Failed command hints:")
        lines.append(_bullet_list(report.failed_command_hints, "No failed command hints detected."))
    if report.tracebacks:
        lines.append("")
        lines.append("Tracebacks:")
        for block in report.tracebacks:
            lines.append("")
            lines.append("```text")
            lines.append(block)
            lines.append("```")
    return "\n".join(lines)


def _pr_comment(report: Report) -> str:
    status = "No errors detected" if not report.errors else f"{len(report.errors)} error line(s) detected"
    tests = report.test_summary or "No test summary detected"
    changed = len(report.changed_files)
    suggestions = report.suggested_next_steps[:3]
    lines = [
        f"Agent run report for `{report.branch}` at `{report.commit}`.",
        f"Changed files: {changed}.",
        f"Status: {status}.",
        f"Tests: {tests}.",
    ]
    if suggestions:
        lines.append("Next steps: " + "; ".join(suggestions))
    return "\n".join(f"> {line}" for line in lines)


def _bullet_list(items: list[str], empty_note: str) -> str:
    if not items:
        return empty_note
    return "\n".join(f"- {item}" for item in items)


def _code_or_note(text: str, empty_note: str) -> str:
    if not text.strip():
        return empty_note
    return f"```text\n{text}\n```"
