"""Unit tests for mld_snooping_clear_statistics module."""

from mld_snooping_clear_statistics import _build_commands


def test_clear_all():
    assert _build_commands("all", None, None) == ["clear ipv6 mld snooping statistics all"]


def test_clear_vlan():
    assert _build_commands("vlan", 10, None) == ["clear ipv6 mld snooping statistics vlan 10"]


def test_clear_interface():
    assert _build_commands("interface", None, "eth1/0/1") == ["clear ipv6 mld snooping statistics interface eth1/0/1"]
