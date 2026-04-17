"""Unit tests for crypto_pki_trustpoint module command builder."""

from crypto_pki_trustpoint import _build_commands


def test_create():
    assert _build_commands("TP1", "present") == [
        "crypto pki trustpoint TP1",
        "exit",
    ]


def test_delete():
    assert _build_commands("TP1", "absent") == [
        "no crypto pki trustpoint TP1",
    ]
