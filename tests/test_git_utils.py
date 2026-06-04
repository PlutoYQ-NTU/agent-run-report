from agent_run_report.git_utils import parse_changed_files


def test_parse_changed_files_handles_common_status_lines():
    status = "\n".join(
        [
            " M README.md",
            "A  src/new_file.py",
            "?? tests/test_new.py",
            "R  old_name.py -> new_name.py",
        ]
    )

    assert parse_changed_files(status) == [
        "README.md",
        "src/new_file.py",
        "tests/test_new.py",
        "new_name.py",
    ]
