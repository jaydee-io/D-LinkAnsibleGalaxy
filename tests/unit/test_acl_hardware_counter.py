"""Unit tests for acl_hardware_counter module command builder."""

from acl_hardware_counter import _build_commands


def test_enable():
    assert _build_commands("abc", "enabled") == ["acl-hardware-counter access-group abc"]


def test_disable():
    assert _build_commands("abc", "disabled") == ["no acl-hardware-counter access-group abc"]


def test_numeric():
    assert _build_commands("3999", "enabled") == ["acl-hardware-counter access-group 3999"]
