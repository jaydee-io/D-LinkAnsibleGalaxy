"""Unit tests for dhcp_snooping_info_allow_untrusted module command builder."""

from dhcp_snooping_info_allow_untrusted import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["ip dhcp snooping information option allow-untrusted"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no ip dhcp snooping information option allow-untrusted"]
