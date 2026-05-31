import json

from agent_run_report.json_writer import render_json
from agent_run_report.report_model import LogFindings, Report, build_suggested_next_steps


def test_log_findings_to_dict_is_json_compatible():
    findings = LogFindings(errors=["error"], warnings=["warning"], test_summary="1 failed")

    payload = findings.to_dict()

    assert payload["errors"] == ["error"]
    json.dumps(payload)


def test_report_model_can_serialize_to_json_compatible_dict():
    report = Report(
        title="Agent Run Report",
        repo_path="/repo",
        branch="main",
        commit="abc123",
        status_short="",
        changed_files=[],
        diff_stat="",
    )

    payload = report.to_dict()

    assert payload["title"] == "Agent Run Report"
    assert payload["changed_files"] == []
    json.dumps(payload)
    assert render_json(report).startswith("{")


def test_suggested_next_steps_for_errors_and_failed_tests(tmp_path):
    suggestions = build_suggested_next_steps(
        errors=["L1: error"],
        test_summary="1 failed, 2 passed",
        changed_files=["src/app.py"],
        repo_path=str(tmp_path),
    )

    assert any("Fix detected errors" in item for item in suggestions)
    assert any("Rerun the failing test" in item for item in suggestions)
    assert any("README" in item for item in suggestions)
