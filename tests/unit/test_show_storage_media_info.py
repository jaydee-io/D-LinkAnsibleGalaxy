"""Unit tests for show_storage_media_info module."""

from show_storage_media_info import _build_command


def test_build_command():
    assert _build_command() == "show storage media-info"
