"""Unit tests for dhcp_snooping_clear_database_stats module command builder."""

from dhcp_snooping_clear_database_stats import _build_commands


def test_clear():
    cmds = _build_commands()
    assert cmds == ["clear ip dhcp snooping database statistics"]
