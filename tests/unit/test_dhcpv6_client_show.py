"""Unit tests for dhcpv6_client_show module command builder."""

from dhcpv6_client_show import _build_command


def test_show_all():
    cmd = _build_command(None)
    assert cmd == "show ipv6 dhcp"


def test_show_interface():
    cmd = _build_command("vlan1")
    assert cmd == "show ipv6 dhcp interface vlan1"
