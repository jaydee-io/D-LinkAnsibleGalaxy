"""Unit tests for crypto_key_zeroize module command builder."""

from crypto_key_zeroize import _build_commands


def test_zeroize_rsa():
    assert _build_commands("rsa") == [
        "crypto key zeroize rsa",
    ]


def test_zeroize_dsa():
    assert _build_commands("dsa") == [
        "crypto key zeroize dsa",
    ]
