"""Unit tests for poe_pd_legacy_support module command builder."""

from poe_pd_legacy_support import _build_commands


def test_enable():
    assert _build_commands("eth1/0/1", "enabled") == [
        "interface eth1/0/1",
        "poe pd legacy-support",
        "exit",
    ]


def test_disable():
    assert _build_commands("eth1/0/1", "disabled") == [
        "interface eth1/0/1",
        "no poe pd legacy-support",
        "exit",
    ]
