"""Structured data models for agent run reports."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class LogFindings:
    """Parsed findings extracted from an optional agent log."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    tracebacks: list[str] = field(default_factory=list)
    test_summary: str = ""
    failed_command_hints: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible representation."""
        return {
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "tracebacks": list(self.tracebacks),
            "test_summary": self.test_summary,
            "failed_command_hints": list(self.failed_command_hints),
        }


@dataclass(slots=True)
class Report:
    """Complete report payload used by Markdown and JSON writers."""

    title: str
    repo_path: str
    branch: str
    commit: str
    status_short: str
    changed_files: list[str]
    diff_stat: str
    log_path: str | None = None
    log_excerpt: str = ""
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    tracebacks: list[str] = field(default_factory=list)
    test_summary: str = ""
    failed_command_hints: list[str] = field(default_factory=list)
    suggested_next_steps: list[str] = field(default_factory=list)
    diff_excerpt: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible report dictionary."""
        return {
            "title": self.title,
            "repo_path": self.repo_path,
            "branch": self.branch,
            "commit": self.commit,
            "status_short": self.status_short,
            "changed_files": list(self.changed_files),
            "diff_stat": self.diff_stat,
            "log_path": self.log_path,
            "log_excerpt": self.log_excerpt,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "tracebacks": list(self.tracebacks),
            "test_summary": self.test_summary,
            "failed_command_hints": list(self.failed_command_hints),
            "suggested_next_steps": list(self.suggested_next_steps),
            "diff_excerpt": self.diff_excerpt,
        }


def build_suggested_next_steps(
    *,
    errors: list[str],
    test_summary: str,
    changed_files: list[str],
    repo_path: str,
) -> list[str]:
    """Build simple rule-based next-step suggestions for maintainers."""
    suggestions: list[str] = []
    test_summary_lower = test_summary.lower()
    tests_detected = bool(test_summary.strip())
    tests_failed = "failed" in test_summary_lower or "failure" in test_summary_lower

    if errors:
        suggestions.append("Fix detected errors before handing off or opening a PR.")
    if tests_failed:
        suggestions.append("Rerun the failing test command after fixes.")
    if changed_files and not tests_detected:
        suggestions.append("Run the relevant test suite because changed files were detected but no test output was found.")
    if not Path(repo_path, "README.md").exists():
        suggestions.append("Add or update README documentation for the repository.")
    if len(changed_files) >= 10:
        suggestions.append("Review the diff carefully because many files changed.")
    if not suggestions:
        suggestions.append("Perform a final manual review and commit when ready.")

    return suggestions
