"""Unit tests for power_saving_shutdown_time_range module command builder."""

from power_saving_shutdown_time_range import _build_commands


def test_add():
    assert _build_commands("eth1/0/1", "off-duty", "present") == [
        "interface eth1/0/1",
        "power-saving shutdown time-range off-duty",
        "exit",
    ]


def test_remove():
    assert _build_commands("eth1/0/1", "off-duty", "absent") == [
        "interface eth1/0/1",
        "no power-saving shutdown time-range off-duty",
        "exit",
    ]
