"""Unit tests for show_ssh module command builder."""

from show_ssh import _build_command


def test_show():
    assert _build_command() == "show ssh"
