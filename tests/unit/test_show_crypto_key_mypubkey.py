"""Unit tests for show_crypto_key_mypubkey module command builder."""

from show_crypto_key_mypubkey import _build_command


def test_show_rsa():
    assert _build_command("rsa") == "show crypto key mypubkey rsa"


def test_show_dsa():
    assert _build_command("dsa") == "show crypto key mypubkey dsa"
