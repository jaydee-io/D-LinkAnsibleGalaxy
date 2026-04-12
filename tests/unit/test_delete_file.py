"""Unit tests for delete_file module."""

from delete_file import _build_commands


def test_delete():
    assert _build_commands("Image2") == ["delete Image2"]


def test_delete_config():
    assert _build_commands("Config1") == ["delete Config1"]
