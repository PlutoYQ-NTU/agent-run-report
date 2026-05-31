"""Helpers for collecting local Git repository information."""

from __future__ import annotations

import subprocess
from pathlib import Path


class GitError(RuntimeError):
    """Raised when a git command fails."""


def validate_repo_path(path: str) -> Path:
    """Resolve and validate a repository path."""
    repo = Path(path).expanduser().resolve()
    if not repo.exists():
        raise ValueError(f"Repository path does not exist: {repo}")
    if not repo.is_dir():
        raise ValueError(f"Repository path is not a directory: {repo}")
    return repo


def is_git_repository(repo: Path) -> bool:
    """Return True if the path is inside a Git working tree."""
    result = _run_git(repo, ["rev-parse", "--is-inside-work-tree"], check=False)
    return result.returncode == 0 and result.stdout.strip().lower() == "true"


def collect_git_info(repo: Path, *, include_diff: bool = False, max_diff_lines: int = 200) -> dict[str, object]:
    """Collect branch, commit, status, changed files, diff stat, and optional diff excerpt."""
    branch = _git_stdout(repo, ["branch", "--show-current"]) or "(detached HEAD)"
    commit = _git_stdout(repo, ["rev-parse", "--short", "HEAD"], default="(no commits)")
    status_short = _git_stdout(repo, ["status", "--short"], default="")
    changed_files = parse_changed_files(status_short)
    diff_stat = _git_stdout(repo, ["diff", "--stat"], default="")
    if not diff_stat and changed_files:
        diff_stat = "No unstaged diff stat available. Some changes may be staged or untracked."

    diff_excerpt = ""
    if include_diff:
        diff_text = _git_stdout(repo, ["diff"], default="")
        diff_excerpt = limit_lines(diff_text, max_diff_lines)

    return {
        "branch": branch,
        "commit": commit,
        "status_short": status_short,
        "changed_files": changed_files,
        "diff_stat": diff_stat,
        "diff_excerpt": diff_excerpt,
    }


def parse_changed_files(status_short: str) -> list[str]:
    """Parse file paths from `git status --short` output."""
    files: list[str] = []
    for line in status_short.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip() if len(line) > 3 else line.strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        files.append(path)
    return files


def limit_lines(text: str, max_lines: int) -> str:
    """Return text limited to max_lines with a truncation notice."""
    if max_lines <= 0:
        return ""
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text
    visible = lines[:max_lines]
    visible.append(f"... truncated after {max_lines} line(s) ...")
    return "\n".join(visible)


def _git_stdout(repo: Path, args: list[str], *, default: str | None = None) -> str:
    result = _run_git(repo, args, check=default is None)
    if result.returncode != 0:
        return default or ""
    return result.stdout.strip()


def _run_git(repo: Path, args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    command = ["git", *args]
    result = subprocess.run(
        command,
        cwd=str(repo),
        text=True,
        capture_output=True,
        check=False,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        raise GitError(f"git {' '.join(args)} failed: {detail}")
    return result
