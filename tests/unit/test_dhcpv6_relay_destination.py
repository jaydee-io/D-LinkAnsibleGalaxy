"""Unit tests for dhcpv6_relay_destination module command builder."""

from dhcpv6_relay_destination import _build_commands


def test_add():
    cmds = _build_commands("vlan1", "FE80::250:A2FF:FEBF:A056", None, "present")
    assert cmds == ["interface vlan1", "ipv6 dhcp relay destination FE80::250:A2FF:FEBF:A056", "exit"]


def test_add_with_output_interface():
    cmds = _build_commands("vlan1", "FE80::250:A2FF:FEBF:A056", "vlan1", "present")
    assert cmds == ["interface vlan1", "ipv6 dhcp relay destination FE80::250:A2FF:FEBF:A056 vlan1", "exit"]


def test_remove():
    cmds = _build_commands("vlan1", "FE80::22:33", None, "absent")
    assert cmds == ["interface vlan1", "no ipv6 dhcp relay destination FE80::22:33", "exit"]
