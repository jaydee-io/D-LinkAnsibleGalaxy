"""Unit tests for dhcp_relay_option_hex module command builder."""

from dhcp_relay_option_hex import _build_commands


def test_add_option():
    cmds = _build_commands("Service-A", 60, "112233", False, None, "present")
    assert cmds == ["ip dhcp class Service-A", "option 60 hex 112233", "exit"]


def test_add_with_wildcard():
    cmds = _build_commands("Service-A", 60, "112233", True, None, "present")
    assert cmds == ["ip dhcp class Service-A", "option 60 hex 112233 *", "exit"]


def test_add_with_bitmask():
    cmds = _build_commands("Service-A", 60, "112233", False, "FF00FF", "present")
    assert cmds == ["ip dhcp class Service-A", "option 60 hex 112233 bitmask FF00FF", "exit"]


def test_remove():
    cmds = _build_commands("Service-A", 60, "112233", False, None, "absent")
    assert cmds == ["ip dhcp class Service-A", "no option 60 hex 112233", "exit"]
