"""Unit tests for mac_auth_system_auth_control module."""

from mac_auth_system_auth_control import _build_commands


def test_enable():
    assert _build_commands("enabled") == ["mac-auth system-auth-control"]


def test_disable():
    assert _build_commands("disabled") == ["no mac-auth system-auth-control"]
