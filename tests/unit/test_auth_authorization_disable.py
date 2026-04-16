"""Unit tests for auth_authorization_disable module command builder."""

from auth_authorization_disable import _build_commands


def test_enable():
    assert _build_commands("enabled") == ["no authorization disable"]


def test_disable():
    assert _build_commands("disabled") == ["authorization disable"]
