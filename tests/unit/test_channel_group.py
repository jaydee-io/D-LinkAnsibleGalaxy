"""Unit tests for channel_group module."""

from channel_group import _build_commands


def test_present_active():
    assert _build_commands("eth1/0/4", 3, "active", "present") == [
        "interface eth1/0/4",
        "channel-group 3 mode active",
        "exit",
    ]


def test_present_on():
    assert _build_commands("eth1/0/4", 1, "on", "present") == [
        "interface eth1/0/4",
        "channel-group 1 mode on",
        "exit",
    ]


def test_present_passive():
    assert _build_commands("eth1/0/5", 3, "passive", "present") == [
        "interface eth1/0/5",
        "channel-group 3 mode passive",
        "exit",
    ]


def test_absent():
    assert _build_commands("eth1/0/4", None, None, "absent") == [
        "interface eth1/0/4",
        "no channel-group",
        "exit",
    ]
