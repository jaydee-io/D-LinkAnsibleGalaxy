"""Unit tests for port_security_clear module command builder."""

from port_security_clear import _build_commands


def test_all():
    assert _build_commands("all", None, None, None) == ["clear port-security all"]


def test_address():
    assert _build_commands("address", "0080.0070.0007", None, None) == [
        "clear port-security address 0080.0070.0007"
    ]


def test_address_vlan():
    assert _build_commands("address", "0080.0070.0007", None, 10) == [
        "clear port-security address 0080.0070.0007 vlan 10"
    ]


def test_interface():
    assert _build_commands("interface", None, "eth1/0/1", None) == [
        "clear port-security interface eth1/0/1"
    ]


def test_interface_vlan():
    assert _build_commands("interface", None, "eth1/0/1", 10) == [
        "clear port-security interface eth1/0/1 vlan 10"
    ]
