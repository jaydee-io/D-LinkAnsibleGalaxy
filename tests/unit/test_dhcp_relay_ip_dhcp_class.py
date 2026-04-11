"""Unit tests for dhcp_relay_ip_dhcp_class module command builder."""

from dhcp_relay_ip_dhcp_class import _build_commands


def test_create():
    cmds = _build_commands("Service-A", "present")
    assert cmds == ["ip dhcp class Service-A"]


def test_delete():
    cmds = _build_commands("Service-A", "absent")
    assert cmds == ["no ip dhcp class Service-A"]
