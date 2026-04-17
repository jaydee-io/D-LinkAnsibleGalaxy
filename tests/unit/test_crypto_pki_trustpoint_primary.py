"""Unit tests for crypto_pki_trustpoint_primary module command builder."""

from crypto_pki_trustpoint_primary import _build_commands


def test_set_primary():
    assert _build_commands("TP1", "present") == [
        "crypto pki trustpoint TP1",
        "primary",
        "exit",
    ]


def test_unset_primary():
    assert _build_commands("TP1", "absent") == [
        "crypto pki trustpoint TP1",
        "no primary",
        "exit",
    ]
