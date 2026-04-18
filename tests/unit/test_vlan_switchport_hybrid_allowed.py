"""Unit tests for vlan_switchport_hybrid_allowed module."""

from vlan_switchport_hybrid_allowed import _build_commands


def test_add_tagged():
    assert _build_commands("eth1/0/1", "add", "tagged", "1000", "present") == [
        "interface eth1/0/1", "switchport hybrid allowed vlan add tagged 1000", "exit"]


def test_add_untagged():
    assert _build_commands("eth1/0/1", "add", "untagged", "2000,3000", "present") == [
        "interface eth1/0/1", "switchport hybrid allowed vlan add untagged 2000,3000", "exit"]


def test_remove():
    assert _build_commands("eth1/0/1", "remove", None, "1000", "present") == [
        "interface eth1/0/1", "switchport hybrid allowed vlan remove 1000", "exit"]


def test_set_tagged():
    assert _build_commands("eth1/0/1", "set", "tagged", "1000", "present") == [
        "interface eth1/0/1", "switchport hybrid allowed vlan tagged 1000", "exit"]


def test_absent():
    assert _build_commands("eth1/0/1", "add", None, "1000", "absent") == [
        "interface eth1/0/1", "no switchport hybrid allowed vlan", "exit"]
