"""Unit tests for dos_prevention module command builder."""

from dos_prevention import _build_commands


def test_enable_land():
    cmds = _build_commands("land", "enabled")
    assert cmds == ["dos-prevention land"]


def test_enable_all():
    cmds = _build_commands("all", "enabled")
    assert cmds == ["dos-prevention all"]


def test_disable_all():
    cmds = _build_commands("all", "disabled")
    assert cmds == ["no dos-prevention all"]


def test_disable_blat():
    cmds = _build_commands("blat", "disabled")
    assert cmds == ["no dos-prevention blat"]
