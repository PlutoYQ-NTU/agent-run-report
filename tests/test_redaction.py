from agent_run_report.redaction import redact_text


def test_redact_text_masks_common_token_like_patterns():
    text = (
        "api_key=example-secret-value "
        "Authorization: Bearer abcdefghijklmnopqrstuvwxyz "
        "token: local-token-value"
    )

    redacted = redact_text(text)

    assert "example-secret-value" not in redacted
    assert "abcdefghijklmnopqrstuvwxyz" not in redacted
    assert "local-token-value" not in redacted
    assert "[REDACTED]" in redacted
