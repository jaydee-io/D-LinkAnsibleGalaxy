"""Unit tests for vlan_switchport_trunk_native module."""

from vlan_switchport_trunk_native import _build_commands


def test_set_vlan():
    assert _build_commands("eth1/0/1", 20, False, "present") == [
        "interface eth1/0/1", "switchport trunk native vlan 20", "exit"]


def test_set_tag():
    assert _build_commands("eth1/0/1", None, True, "present") == [
        "interface eth1/0/1", "switchport trunk native vlan tag", "exit"]


def test_absent():
    assert _build_commands("eth1/0/1", None, False, "absent") == [
        "interface eth1/0/1", "no switchport trunk native vlan", "exit"]
