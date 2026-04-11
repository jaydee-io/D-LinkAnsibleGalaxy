"""Unit tests for dhcp_snooping_renew_database module command builder."""

from dhcp_snooping_renew_database import _build_commands


def test_renew():
    cmds = _build_commands("tftp://1.2.3.4/db.txt")
    assert cmds == ["renew ip dhcp snooping database tftp://1.2.3.4/db.txt"]
