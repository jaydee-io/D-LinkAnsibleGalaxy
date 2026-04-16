"""Unit tests for show_port_security module command builder."""

from show_port_security import _build_command


def test_default():
    assert _build_command(None, False) == "show port-security"


def test_interface():
    assert _build_command("eth1/0/1-3", False) == "show port-security interface eth1/0/1-3"


def test_interface_address():
    assert _build_command("eth1/0/1", True) == "show port-security interface eth1/0/1 address"


def test_address_only():
    assert _build_command(None, True) == "show port-security address"
