"""Unit tests for show_interfaces module."""

from show_interfaces import _build_command


def test_all():
    assert _build_command(None) == "show interfaces"


def test_specific_interface():
    assert _build_command("eth1/0/1") == "show interfaces eth1/0/1"


def test_vlan():
    assert _build_command("vlan1") == "show interfaces vlan1"
