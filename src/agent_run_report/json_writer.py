"""JSON rendering for agent run reports."""

from __future__ import annotations

import json

from .report_model import Report


def render_json(report: Report) -> str:
    """Render report data as formatted JSON."""
    return json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n"


def write_json(report: Report, path: str) -> None:
    """Write report data to a JSON file."""
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(render_json(report))
