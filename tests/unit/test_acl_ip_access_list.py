"""Unit tests for ip_access_list module command builder."""

from acl_ip_access_list import _build_commands


def test_create_extended():
    cmds = _build_commands("Strict-Control", None, True, "present")
    assert cmds == ["ip access-list extended Strict-Control", "exit"]


def test_create_standard():
    cmds = _build_commands("pim-srcfilter", None, False, "present")
    assert cmds == ["ip access-list pim-srcfilter", "exit"]


def test_create_with_number():
    cmds = _build_commands("Strict-Control", 3000, True, "present")
    assert cmds == ["ip access-list extended Strict-Control 3000", "exit"]


def test_delete():
    cmds = _build_commands("Strict-Control", None, True, "absent")
    assert cmds == ["no ip access-list extended Strict-Control"]


def test_delete_standard():
    cmds = _build_commands("pim-srcfilter", None, False, "absent")
    assert cmds == ["no ip access-list pim-srcfilter"]
