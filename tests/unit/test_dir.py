"""Unit tests for dir module."""

from dir import _build_command


def test_dir_no_url():
    assert _build_command(None) == "dir"


def test_dir_with_url():
    assert _build_command("Image1") == "dir Image1"
