"""Unit tests for flowcontrol module."""

from flowcontrol import _build_commands


def test_enable():
    assert _build_commands("eth1/0/1", "enabled") == [
        "interface eth1/0/1", "flowcontrol on", "exit"]


def test_disable():
    assert _build_commands("eth1/0/1", "disabled") == [
        "interface eth1/0/1", "flowcontrol off", "exit"]
