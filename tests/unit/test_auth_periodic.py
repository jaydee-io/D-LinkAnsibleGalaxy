"""Unit tests for auth_periodic module command builder."""

from auth_periodic import _build_commands


def test_enable():
    assert _build_commands("eth1/0/1", "enabled") == [
        "interface eth1/0/1",
        "authentication periodic",
        "exit",
    ]


def test_disable():
    assert _build_commands("eth1/0/1", "disabled") == [
        "interface eth1/0/1",
        "no authentication periodic",
        "exit",
    ]
