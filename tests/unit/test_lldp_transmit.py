"""Unit tests for lldp_transmit module."""

from lldp_transmit import _build_commands


def test_enable():
    assert _build_commands("eth1/0/1", "enabled") == [
        "interface eth1/0/1", "lldp transmit", "exit"]


def test_disable():
    assert _build_commands("eth1/0/1", "disabled") == [
        "interface eth1/0/1", "no lldp transmit", "exit"]
