"""Unit tests for dot1x_pae_authenticator module command builder."""

from dot1x_pae_authenticator import _build_commands


def test_enable():
    cmds = _build_commands("eth1/0/1", "enabled")
    assert cmds == ["interface eth1/0/1", "dot1x pae authenticator"]


def test_disable():
    cmds = _build_commands("eth1/0/1", "disabled")
    assert cmds == ["interface eth1/0/1", "no dot1x pae authenticator"]


def test_different_interface():
    cmds = _build_commands("eth1/0/24", "enabled")
    assert cmds == ["interface eth1/0/24", "dot1x pae authenticator"]
