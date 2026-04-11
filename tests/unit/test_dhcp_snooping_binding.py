"""Unit tests for dhcp_snooping_binding module command builder."""

from dhcp_snooping_binding import _build_commands


def test_add_binding():
    cmds = _build_commands("00:11:22:33:44:55", 100, "10.0.0.1", "ethernet 1/0/1", 86400)
    assert cmds == ["ip dhcp snooping binding 00:11:22:33:44:55 vlan 100 10.0.0.1 interface ethernet 1/0/1 expiry 86400"]
