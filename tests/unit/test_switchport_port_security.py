"""Unit tests for switchport_port_security module command builder."""

from switchport_port_security import _build_commands


def test_enable_default():
    assert _build_commands("eth1/0/1", None, None, None, None, None, None, "present") == [
        "interface eth1/0/1",
        "switchport port-security",
        "exit",
    ]


def test_set_maximum():
    assert _build_commands("eth1/0/1", 10, None, None, None, None, None, "present") == [
        "interface eth1/0/1",
        "switchport port-security maximum 10",
        "exit",
    ]


def test_set_violation():
    assert _build_commands("eth1/0/1", None, "shutdown", None, None, None, None, "present") == [
        "interface eth1/0/1",
        "switchport port-security violation shutdown",
        "exit",
    ]


def test_set_mode():
    assert _build_commands("eth1/0/1", None, None, "permanent", None, None, None, "present") == [
        "interface eth1/0/1",
        "switchport port-security mode permanent",
        "exit",
    ]


def test_add_mac():
    assert _build_commands("eth1/0/1", None, None, None, "0080.0070.0007", False, None, "present") == [
        "interface eth1/0/1",
        "switchport port-security mac-address 0080.0070.0007",
        "exit",
    ]


def test_add_permanent_mac_with_vlan():
    assert _build_commands("eth1/0/1", None, None, None, "0080.0070.0007", True, 10, "present") == [
        "interface eth1/0/1",
        "switchport port-security mac-address permanent 0080.0070.0007 vlan 10",
        "exit",
    ]


def test_disable_all():
    assert _build_commands("eth1/0/1", None, None, None, None, None, None, "absent") == [
        "interface eth1/0/1",
        "no switchport port-security",
        "exit",
    ]


def test_remove_maximum():
    assert _build_commands("eth1/0/1", 10, None, None, None, None, None, "absent") == [
        "interface eth1/0/1",
        "no switchport port-security maximum",
        "exit",
    ]


def test_remove_mac():
    assert _build_commands("eth1/0/1", None, None, None, "0080.0070.0007", None, None, "absent") == [
        "interface eth1/0/1",
        "no switchport port-security mac-address 0080.0070.0007",
        "exit",
    ]
