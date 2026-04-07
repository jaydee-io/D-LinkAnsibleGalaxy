"""Unit tests for clear_acl_hardware_counter module command builder."""

from acl_clear_hardware_counter import _build_command


def test_clear_specific():
    assert _build_command("abc") == "clear acl-hardware-counter access-group abc"


def test_clear_all():
    assert _build_command(None) == "clear acl-hardware-counter access-group"
