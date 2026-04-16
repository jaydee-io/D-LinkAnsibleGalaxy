"""Unit tests for auth_timer_restart module command builder."""

from auth_timer_restart import _build_commands


def test_set():
    assert _build_commands("eth1/0/1", 20, "present") == [
        "interface eth1/0/1",
        "authentication timer restart 20",
        "exit",
    ]


def test_reset():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1",
        "no authentication timer restart",
        "exit",
    ]
