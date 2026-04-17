"""Unit tests for crypto_key_generate module command builder."""

from crypto_key_generate import _build_commands


def test_generate_rsa():
    assert _build_commands("rsa", None) == [
        "crypto key generate rsa",
    ]


def test_generate_rsa_modulus():
    assert _build_commands("rsa", 2048) == [
        "crypto key generate rsa modulus 2048",
    ]


def test_generate_dsa():
    assert _build_commands("dsa", None) == [
        "crypto key generate dsa",
    ]
