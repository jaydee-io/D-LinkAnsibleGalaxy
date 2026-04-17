"""Unit tests for show_crypto_pki_trustpoints module command builder."""

from show_crypto_pki_trustpoints import _build_command


def test_show_all():
    assert _build_command(None) == "show crypto pki trustpoints"


def test_show_specific():
    assert _build_command("TP1") == "show crypto pki trustpoints TP1"
