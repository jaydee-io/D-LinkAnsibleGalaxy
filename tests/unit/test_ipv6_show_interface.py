"""Unit tests for ipv6_show_interface module command builder."""

from ipv6_show_interface import _build_command


def test_show_all():
    assert _build_command(None, False) == "show ipv6 interface"


def test_show_interface():
    assert _build_command("vlan1", False) == "show ipv6 interface vlan1"


def test_show_brief():
    assert _build_command(None, True) == "show ipv6 interface brief"


def test_show_interface_brief():
    assert _build_command("vlan1", True) == "show ipv6 interface vlan1 brief"
