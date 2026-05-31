from agent_run_report.log_parser import parse_log_text


def test_log_parser_detects_errors_and_warnings():
    findings = parse_log_text("""
starting job
WARNING: cache miss
command failed with exit code 1
RuntimeError: bad state
""")

    assert any("WARNING" in item for item in findings.warnings)
    assert any("RuntimeError" in item for item in findings.errors)
    assert any("exit code 1" in item for item in findings.failed_command_hints)


def test_traceback_extraction_works():
    findings = parse_log_text("""
Traceback (most recent call last):
  File "app.py", line 1, in <module>
    raise ValueError("bad")
ValueError: bad
next line
""")

    assert len(findings.tracebacks) == 1
    assert "ValueError: bad" in findings.tracebacks[0]
    assert any("Traceback" in item for item in findings.errors)


def test_test_summary_uses_latest_hint():
    findings = parse_log_text("""
pytest tests
== 2 passed, 1 skipped in 0.10s ==
""")

    assert findings.test_summary == "2 passed, 1 skipped in 0.10s"
