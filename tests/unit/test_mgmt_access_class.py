"""Unit tests for mgmt_access_class module command builder."""

from mgmt_access_class import _build_commands


def test_apply():
    cmds = _build_commands("telnet", "vty-filter", "present")
    assert cmds == ["line telnet", "access-class vty-filter", "exit"]


def test_remove():
    cmds = _build_commands("ssh", "vty-filter", "absent")
    assert cmds == ["line ssh", "no access-class vty-filter", "exit"]
