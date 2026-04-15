"""Unit tests for lldp_receive module."""

from lldp_receive import _build_commands


def test_enable():
    assert _build_commands("eth1/0/1", "enabled") == [
        "interface eth1/0/1", "lldp receive", "exit"]


def test_disable():
    assert _build_commands("eth1/0/1", "disabled") == [
        "interface eth1/0/1", "no lldp receive", "exit"]
