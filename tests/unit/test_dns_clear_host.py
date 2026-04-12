"""Unit tests for dns_clear_host module command builder."""

from dns_clear_host import _build_commands


def test_clear_all():
    cmds = _build_commands(None)
    assert cmds == ["clear host all"]


def test_clear_specific():
    cmds = _build_commands("www.abc.com")
    assert cmds == ["clear host www.abc.com"]
