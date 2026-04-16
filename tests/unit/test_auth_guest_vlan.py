"""Unit tests for auth_guest_vlan module command builder."""

from auth_guest_vlan import _build_commands


def test_set():
    assert _build_commands("eth1/0/1", 5, "present") == [
        "interface eth1/0/1",
        "authentication guest-vlan 5",
        "exit",
    ]


def test_remove():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1",
        "no authentication guest-vlan",
        "exit",
    ]
