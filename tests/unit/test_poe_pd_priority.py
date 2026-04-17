"""Unit tests for poe_pd_priority module command builder."""

from poe_pd_priority import _build_commands


def test_set_critical():
    assert _build_commands("eth1/0/1", "critical", "present") == [
        "interface eth1/0/1",
        "poe pd priority critical",
        "exit",
    ]


def test_set_high():
    assert _build_commands("eth1/0/1", "high", "present") == [
        "interface eth1/0/1",
        "poe pd priority high",
        "exit",
    ]


def test_revert():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1",
        "no poe pd priority",
        "exit",
    ]
