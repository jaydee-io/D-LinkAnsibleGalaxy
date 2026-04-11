"""Unit tests for dhcpv6_relay_mac_format module command builder."""

from dhcpv6_relay_mac_format import _build_commands


def test_set_with_number():
    cmds = _build_commands("uppercase", "hyphen", 5, "present")
    assert cmds == ["ipv6 dhcp relay information option mac-format case uppercase delimiter hyphen number 5"]


def test_set_without_number():
    cmds = _build_commands("lowercase", "colon", None, "present")
    assert cmds == ["ipv6 dhcp relay information option mac-format case lowercase delimiter colon"]


def test_reset():
    cmds = _build_commands(None, None, None, "absent")
    assert cmds == ["no ipv6 dhcp relay information option mac-format case"]
