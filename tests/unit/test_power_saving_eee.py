"""Unit tests for power_saving_eee module command builder."""

from power_saving_eee import _build_commands


def test_enable():
    assert _build_commands("eth1/0/1", "enabled") == [
        "interface eth1/0/1",
        "power-saving eee",
        "exit",
    ]


def test_disable():
    assert _build_commands("eth1/0/1", "disabled") == [
        "interface eth1/0/1",
        "no power-saving eee",
        "exit",
    ]
