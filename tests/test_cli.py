from agent_run_report import cli


def test_dry_run_builds_report_without_writing_default_report(capsys):
    code = cli.main(["--repo", ".", "--dry-run"])

    captured = capsys.readouterr()
    assert code == 0
    assert "Dry run: report built" in captured.out
    assert "Markdown output:" in captured.out
