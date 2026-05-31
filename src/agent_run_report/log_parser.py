"""Rule-based parsing for coding-agent log files."""

from __future__ import annotations

import re

from .report_model import LogFindings

_ERROR_MARKERS = ("error", "failed", "failure", "exception")
_WARNING_MARKERS = ("warning", "warn")
_TEST_MARKERS = ("pytest", "passed", "failed", "skipped")
_FAILED_COMMAND_MARKERS = ("failed command", "command failed", "exit code", "exit status", "returned non-zero")
_SUMMARY_RE = re.compile(
    r"(=+\s*)?(?P<summary>.*\b\d+\s+(?:passed|failed|skipped|error|errors|xfailed|xpassed)\b.*)(\s*=+)?$",
    re.IGNORECASE,
)


def parse_log_text(text: str) -> LogFindings:
    """Parse log text and return structured findings.

    The parser is intentionally small and rule-based. It detects common error,
    warning, traceback, failed command, and test-summary hints without trying to
    understand every possible agent or test runner format.
    """
    lines = text.splitlines()
    errors: list[str] = []
    warnings: list[str] = []
    tracebacks: list[str] = []
    failed_command_hints: list[str] = []
    test_summary = ""

    index = 0
    while index < len(lines):
        line = lines[index]
        lower = line.lower()

        if "traceback" in lower:
            block, next_index = _collect_traceback(lines, index)
            tracebacks.append(block)
            errors.append(_format_line(index + 1, line))
            index = next_index
            continue

        if any(marker in lower for marker in _WARNING_MARKERS):
            warnings.append(_format_line(index + 1, line))

        if any(marker in lower for marker in _ERROR_MARKERS):
            errors.append(_format_line(index + 1, line))

        if any(marker in lower for marker in _FAILED_COMMAND_MARKERS):
            failed_command_hints.append(_format_line(index + 1, line))

        summary = _extract_test_summary(line)
        if summary:
            test_summary = summary
        elif any(marker in lower for marker in _TEST_MARKERS):
            test_summary = line.strip()

        index += 1

    return LogFindings(
        errors=_dedupe(errors),
        warnings=_dedupe(warnings),
        tracebacks=tracebacks,
        test_summary=test_summary,
        failed_command_hints=_dedupe(failed_command_hints),
    )


def parse_log_file(path: str) -> LogFindings:
    """Read and parse a UTF-8 compatible log file."""
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return parse_log_text(handle.read())


def _collect_traceback(lines: list[str], start: int) -> tuple[str, int]:
    block: list[str] = []
    index = start
    while index < len(lines):
        line = lines[index]
        if index > start and not line.strip():
            break
        block.append(line)
        if index > start and _looks_like_traceback_end(line):
            index += 1
            break
        index += 1
    return "\n".join(block), index


def _looks_like_traceback_end(line: str) -> bool:
    stripped = line.strip()
    return bool(re.match(r"^[A-Za-z_][\w.]*?(Error|Exception|Warning|Failure):", stripped))


def _extract_test_summary(line: str) -> str:
    match = _SUMMARY_RE.search(line.strip())
    if match:
        return match.group("summary").strip().strip("= ").strip()
    return ""


def _format_line(line_number: int, line: str) -> str:
    return f"L{line_number}: {line.strip()}"


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for item in items:
        if item not in seen:
            unique.append(item)
            seen.add(item)
    return unique
