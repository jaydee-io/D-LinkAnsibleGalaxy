"""Unit tests for config_restore module command builder."""

from config_restore import _build_commands


def test_basic_config():
    config = "interface ethernet 1/0/1\ndescription Test\nexit\n"
    cmds = _build_commands(config)
    assert cmds == ["interface ethernet 1/0/1", "description Test", "exit"]


def test_skip_comments_and_blanks():
    config = "! comment\n\nvlan 10\n! another comment\nname DATA\n"
    cmds = _build_commands(config)
    assert cmds == ["vlan 10", "name DATA"]


def test_empty_config():
    cmds = _build_commands("")
    assert cmds == []


def test_only_comments():
    config = "! line1\n! line2\n"
    cmds = _build_commands(config)
    assert cmds == []
