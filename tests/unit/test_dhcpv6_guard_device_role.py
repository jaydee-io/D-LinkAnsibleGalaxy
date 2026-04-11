"""Unit tests for dhcpv6_guard_device_role module command builder."""

from dhcpv6_guard_device_role import _build_commands


def test_set_server():
    cmds = _build_commands("my-policy", "server", "present")
    assert cmds == ["ipv6 dhcp guard policy my-policy", "device-role server", "exit"]


def test_set_client():
    cmds = _build_commands("my-policy", "client", "present")
    assert cmds == ["ipv6 dhcp guard policy my-policy", "device-role client", "exit"]


def test_remove():
    cmds = _build_commands("my-policy", None, "absent")
    assert cmds == ["ipv6 dhcp guard policy my-policy", "no device-role", "exit"]
