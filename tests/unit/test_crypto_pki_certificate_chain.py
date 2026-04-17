"""Unit tests for crypto_pki_certificate_chain module command builder."""

from crypto_pki_certificate_chain import _build_commands


def test_enter_chain():
    assert _build_commands("TP1") == [
        "crypto pki certificate chain TP1",
        "exit",
    ]
