"""Unit tests for dhcp_snooping_database module command builder."""

from dhcp_snooping_database import _build_commands


def test_set_url():
    cmds = _build_commands("present", "tftp://1.2.3.4/db.txt", None)
    assert cmds == ["ip dhcp snooping database tftp://1.2.3.4/db.txt"]


def test_set_write_delay():
    cmds = _build_commands("present", None, 300)
    assert cmds == ["ip dhcp snooping database write-delay 300"]


def test_remove_database():
    cmds = _build_commands("absent", None, None)
    assert cmds == ["no ip dhcp snooping database"]


def test_remove_write_delay():
    cmds = _build_commands("absent", None, 300)
    assert cmds == ["no ip dhcp snooping database write-delay"]
