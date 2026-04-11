"""Unit tests for dhcpv6_relay_show module command builder."""

from dhcpv6_relay_show import _build_command


def test_show_all():
    cmd = _build_command()
    assert cmd == "show ipv6 dhcp"


def test_show_interface():
    cmd = _build_command(interface="vlan1")
    assert cmd == "show ipv6 dhcp interface vlan1"
