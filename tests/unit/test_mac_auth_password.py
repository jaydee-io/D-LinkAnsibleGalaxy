"""Unit tests for mac_auth_password module."""

from mac_auth_password import _build_commands


def test_set_clear():
    assert _build_commands("newpass", None, "present") == ["mac-auth password newpass"]


def test_set_encrypted():
    assert _build_commands("newpass", 7, "present") == ["mac-auth password 7 newpass"]


def test_reset():
    assert _build_commands(None, None, "absent") == ["no mac-auth password"]
