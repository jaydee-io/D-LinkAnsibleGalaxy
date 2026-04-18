"""Unit tests for vlan_switchport_mode module."""

from vlan_switchport_mode import _build_commands


def test_trunk():
    assert _build_commands("eth1/0/1", "trunk", "present") == [
        "interface eth1/0/1", "switchport mode trunk", "exit"]


def test_access():
    assert _build_commands("eth1/0/1", "access", "present") == [
        "interface eth1/0/1", "switchport mode access", "exit"]


def test_absent():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1", "no switchport mode", "exit"]
