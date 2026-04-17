"""Unit tests for poe_power_inline module command builder."""

from poe_power_inline import _build_commands


def test_auto():
    assert _build_commands("eth1/0/1", "auto", None, None, "present") == [
        "interface eth1/0/1",
        "poe power-inline auto",
        "exit",
    ]


def test_auto_max():
    assert _build_commands("eth1/0/1", "auto", 7000, None, "present") == [
        "interface eth1/0/1",
        "poe power-inline auto max 7000",
        "exit",
    ]


def test_auto_time_range():
    assert _build_commands("eth1/0/1", "auto", None, "day-time", "present") == [
        "interface eth1/0/1",
        "poe power-inline auto time-range day-time",
        "exit",
    ]


def test_auto_max_time_range():
    assert _build_commands("eth1/0/1", "auto", 5000, "day-time", "present") == [
        "interface eth1/0/1",
        "poe power-inline auto max 5000 time-range day-time",
        "exit",
    ]


def test_never():
    assert _build_commands("eth1/0/1", "never", None, None, "present") == [
        "interface eth1/0/1",
        "poe power-inline never",
        "exit",
    ]


def test_revert():
    assert _build_commands("eth1/0/1", None, None, None, "absent") == [
        "interface eth1/0/1",
        "no poe power-inline",
        "exit",
    ]
