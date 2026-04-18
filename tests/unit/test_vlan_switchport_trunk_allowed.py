"""Unit tests for vlan_switchport_trunk_allowed module."""

from vlan_switchport_trunk_allowed import _build_commands


def test_add():
    assert _build_commands("eth1/0/1", "add", "1000", "present") == [
        "interface eth1/0/1", "switchport trunk allowed vlan add 1000", "exit"]


def test_all():
    assert _build_commands("eth1/0/1", "all", None, "present") == [
        "interface eth1/0/1", "switchport trunk allowed vlan all", "exit"]


def test_remove():
    assert _build_commands("eth1/0/1", "remove", "1000", "present") == [
        "interface eth1/0/1", "switchport trunk allowed vlan remove 1000", "exit"]


def test_except():
    assert _build_commands("eth1/0/1", "except", "100-200", "present") == [
        "interface eth1/0/1", "switchport trunk allowed vlan except 100-200", "exit"]


def test_absent():
    assert _build_commands("eth1/0/1", "add", None, "absent") == [
        "interface eth1/0/1", "no switchport trunk allowed vlan", "exit"]
