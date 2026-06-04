"""Command line interface for agent-run-report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .git_utils import GitError, collect_git_info, is_git_repository, validate_repo_path
from .json_writer import write_json
from .log_parser import parse_log_file
from .markdown_writer import write_markdown
from .redaction import redact_report
from .report_model import LogFindings, Report, build_suggested_next_steps


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="agent-run-report",
        description="Generate Markdown and JSON reports from local coding-agent runs.",
    )
    parser.add_argument("--repo", default=".", help="Repository path. Default: current directory.")
    parser.add_argument("--log", dest="log_path", help="Optional agent log file.")
    parser.add_argument("--out", default="reports/run_report.md", help="Markdown report output path.")
    parser.add_argument("--json-out", help="Optional JSON report output path.")
    parser.add_argument("--include-diff", action="store_true", help="Include a diff excerpt in the report.")
    parser.add_argument("--max-diff-lines", type=int, default=200, help="Max lines of full diff excerpt.")
    parser.add_argument("--title", default="Agent Run Report", help="Optional report title.")
    parser.add_argument("--no-next-steps", action="store_true", help="Disable automatic next-step suggestions.")
    parser.add_argument("--redact", action="store_true", help="Redact common token-like strings from report text fields.")
    parser.add_argument("--dry-run", action="store_true", help="Build the report and print a summary without writing files.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command line program."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        report = build_report(args)
        if args.redact:
            report = redact_report(report)
        if args.dry_run:
            print(f"Dry run: report built for {report.repo_path}")
            print(f"Changed files: {len(report.changed_files)}")
            print(f"Markdown output: {args.out}")
            if args.json_out:
                print(f"JSON output: {args.json_out}")
            return 0
        _ensure_parent(args.out)
        write_markdown(report, args.out)
        if args.json_out:
            _ensure_parent(args.json_out)
            write_json(report, args.json_out)
    except (ValueError, OSError, GitError) as exc:
        print(f"agent-run-report: error: {exc}", file=sys.stderr)
        return 2

    print(f"Markdown report written to {Path(args.out).resolve()}")
    if args.json_out:
        print(f"JSON report written to {Path(args.json_out).resolve()}")
    return 0


def build_report(args: argparse.Namespace) -> Report:
    """Build a report from parsed CLI arguments."""
    repo = validate_repo_path(args.repo)
    if not is_git_repository(repo):
        raise ValueError(f"Repository path is not a Git working tree: {repo}")
    if args.max_diff_lines < 0:
        raise ValueError("--max-diff-lines must be greater than or equal to 0")

    git_info = collect_git_info(repo, include_diff=args.include_diff, max_diff_lines=args.max_diff_lines)
    findings = _read_log_findings(args.log_path)
    changed_files = list(git_info["changed_files"])

    if args.no_next_steps:
        suggested_next_steps: list[str] = []
    else:
        suggested_next_steps = build_suggested_next_steps(
            errors=findings.errors,
            test_summary=findings.test_summary,
            changed_files=changed_files,
            repo_path=str(repo),
        )

    return Report(
        title=args.title,
        repo_path=str(repo),
        branch=str(git_info["branch"]),
        commit=str(git_info["commit"]),
        status_short=str(git_info["status_short"]),
        changed_files=changed_files,
        diff_stat=str(git_info["diff_stat"]),
        log_path=str(Path(args.log_path).expanduser().resolve()) if args.log_path else None,
        log_excerpt=_read_log_excerpt(args.log_path),
        errors=findings.errors,
        warnings=findings.warnings,
        tracebacks=findings.tracebacks,
        test_summary=findings.test_summary,
        failed_command_hints=findings.failed_command_hints,
        suggested_next_steps=suggested_next_steps,
        diff_excerpt=str(git_info["diff_excerpt"]),
    )


def _read_log_findings(log_path: str | None) -> LogFindings:
    if not log_path:
        return LogFindings()
    path = Path(log_path).expanduser().resolve()
    if not path.exists():
        raise ValueError(f"Log file does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"Log path is not a file: {path}")
    return parse_log_file(str(path))


def _read_log_excerpt(log_path: str | None, *, max_chars: int = 4000) -> str:
    if not log_path:
        return ""
    path = Path(log_path).expanduser().resolve()
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n... truncated ..."


def _ensure_parent(path: str) -> None:
    parent = Path(path).expanduser().resolve().parent
    parent.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
