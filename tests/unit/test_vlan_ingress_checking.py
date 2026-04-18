"""Unit tests for vlan_ingress_checking module."""

from vlan_ingress_checking import _build_commands


def test_enable():
    assert _build_commands("eth1/0/1", "enabled") == [
        "interface eth1/0/1", "ingress-checking", "exit"]


def test_disable():
    assert _build_commands("eth1/0/1", "disabled") == [
        "interface eth1/0/1", "no ingress-checking", "exit"]
