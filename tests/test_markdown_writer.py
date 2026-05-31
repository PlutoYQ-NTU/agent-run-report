from agent_run_report.markdown_writer import render_markdown
from agent_run_report.report_model import Report


def test_markdown_writer_includes_expected_sections():
    report = Report(
        title="Agent Run Report",
        repo_path="/repo",
        branch="main",
        commit="abc123",
        status_short=" M src/app.py",
        changed_files=["src/app.py"],
        diff_stat="src/app.py | 2 ++",
        errors=[],
        warnings=[],
        test_summary="1 passed",
        suggested_next_steps=["Perform a final manual review and commit when ready."],
    )

    markdown = render_markdown(report)

    assert "# Agent Run Report" in markdown
    assert "## Summary" in markdown
    assert "## Repository" in markdown
    assert "## Changed Files" in markdown
    assert "## Diff Stat" in markdown
    assert "## Log Findings" in markdown
    assert "## Errors" in markdown
    assert "## Warnings" in markdown
    assert "## Test Summary" in markdown
    assert "## Diff Excerpt" in markdown
    assert "## Suggested Next Steps" in markdown
    assert "## PR / Issue Comment" in markdown
    assert "No errors detected in the provided log." in markdown
