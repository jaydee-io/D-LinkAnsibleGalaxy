"""Unit tests for auth_timer_reauthentication module command builder."""

from auth_timer_reauthentication import _build_commands


def test_set():
    assert _build_commands("eth1/0/1", 200, "present") == [
        "interface eth1/0/1",
        "authentication timer reauthentication 200",
        "exit",
    ]


def test_reset():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1",
        "no authentication timer reauthentication",
        "exit",
    ]
