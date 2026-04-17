"""Unit tests for crypto_pki_certificate_generate module command builder."""

from crypto_pki_certificate_generate import _build_commands


def test_generate():
    assert _build_commands() == [
        "crypto pki certificate generate",
    ]
