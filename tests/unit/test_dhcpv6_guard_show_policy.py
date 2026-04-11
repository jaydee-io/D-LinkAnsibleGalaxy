"""Unit tests for dhcpv6_guard_show_policy module command builder."""

from dhcpv6_guard_show_policy import _build_command


def test_show_all():
    cmd = _build_command(None)
    assert cmd == "show ipv6 dhcp guard policy"


def test_show_named():
    cmd = _build_command("my-policy")
    assert cmd == "show ipv6 dhcp guard policy my-policy"
