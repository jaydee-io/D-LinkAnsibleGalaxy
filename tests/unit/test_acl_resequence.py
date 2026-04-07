"""Unit tests for access_list_resequence module command builder."""

from acl_resequence import _build_commands


def test_resequence():
    cmds = _build_commands("R&D", 1, 2, "present")
    assert cmds == ["access-list resequence R&D 1 2"]


def test_resequence_numeric():
    cmds = _build_commands("3552", 10, 10, "present")
    assert cmds == ["access-list resequence 3552 10 10"]


def test_revert():
    cmds = _build_commands("R&D", None, None, "absent")
    assert cmds == ["no access-list resequence"]
