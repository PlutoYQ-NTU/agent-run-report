"""Redaction helpers for report text fields."""

from __future__ import annotations

import re
from dataclasses import replace

from .report_model import Report


REDACTION_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"), "sk-[REDACTED]"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AKIA[REDACTED]"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"), "gh_[REDACTED]"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"), "xox-[REDACTED]"),
    (re.compile(r"(?i)\b(bearer\s+)[A-Za-z0-9._~+/=-]{20,}"), r"\1[REDACTED]"),
    (re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[^'\"\s]+"), r"\1=[REDACTED]"),
)


def redact_text(text: str) -> str:
    """Redact common token-like substrings from text."""
    redacted = text
    for pattern, replacement in REDACTION_PATTERNS:
        redacted = pattern.sub(replacement, redacted)
    return redacted


def redact_lines(lines: list[str]) -> list[str]:
    """Redact a list of text lines."""
    return [redact_text(line) for line in lines]


def redact_report(report: Report) -> Report:
    """Return a copy of a report with common token-like strings redacted."""
    return replace(
        report,
        status_short=redact_text(report.status_short),
        changed_files=redact_lines(report.changed_files),
        diff_stat=redact_text(report.diff_stat),
        log_excerpt=redact_text(report.log_excerpt),
        errors=redact_lines(report.errors),
        warnings=redact_lines(report.warnings),
        tracebacks=redact_lines(report.tracebacks),
        test_summary=redact_text(report.test_summary),
        failed_command_hints=redact_lines(report.failed_command_hints),
        diff_excerpt=redact_text(report.diff_excerpt),
    )
