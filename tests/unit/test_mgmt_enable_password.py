"""Unit tests for mgmt_enable_password module command builder."""

from mgmt_enable_password import _build_commands


def test_set_plain():
    assert _build_commands("MyPass", None, "present") == ["enable password MyPass"]


def test_set_encrypted():
    assert _build_commands("MyPass", 7, "present") == ["enable password 7 MyPass"]


def test_remove():
    assert _build_commands(None, None, "absent") == ["no enable password"]
