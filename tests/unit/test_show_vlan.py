"""Unit tests for show_vlan module."""

from show_vlan import _build_command


def test_all():
    assert _build_command(None, None) == "show vlan"


def test_vlan_id():
    assert _build_command("100", None) == "show vlan 100"


def test_interface():
    assert _build_command(None, "eth1/0/1-2") == "show vlan interface eth1/0/1-2"
