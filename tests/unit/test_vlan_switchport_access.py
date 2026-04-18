"""Unit tests for vlan_switchport_access module."""

from vlan_switchport_access import _build_commands


def test_set():
    assert _build_commands("eth1/0/1", 1000, "present") == [
        "interface eth1/0/1", "switchport access vlan 1000", "exit"]


def test_absent():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1", "no switchport access vlan", "exit"]
