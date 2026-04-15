"""Unit tests for mac_auth_username module."""

from mac_auth_username import _build_commands


def test_set():
    assert _build_commands("user1", "present") == ["mac-auth username user1"]


def test_reset():
    assert _build_commands(None, "absent") == ["no mac-auth username"]
