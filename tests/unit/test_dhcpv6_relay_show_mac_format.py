"""Unit tests for dhcpv6_relay_show_mac_format module command builder."""

from dhcpv6_relay_show_mac_format import _build_command


def test_show():
    cmd = _build_command()
    assert cmd == "show ipv6 dhcp relay information option mac-format"
