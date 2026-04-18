"""Unit tests for vlan_switchport_hybrid_native module."""

from vlan_switchport_hybrid_native import _build_commands


def test_set():
    assert _build_commands("eth1/0/1", 20, "present") == [
        "interface eth1/0/1", "switchport hybrid native vlan 20", "exit"]


def test_absent():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1", "no switchport hybrid native vlan", "exit"]
