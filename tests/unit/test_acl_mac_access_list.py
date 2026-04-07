"""Unit tests for mac_access_list module command builder."""

from acl_mac_access_list import _build_commands


def test_create():
    cmds = _build_commands("daily-profile", None, "present")
    assert cmds == ["mac access-list extended daily-profile", "exit"]


def test_create_with_number():
    cmds = _build_commands("daily-profile", 7000, "present")
    assert cmds == ["mac access-list extended daily-profile 7000", "exit"]


def test_delete():
    cmds = _build_commands("daily-profile", None, "absent")
    assert cmds == ["no mac access-list extended daily-profile"]
