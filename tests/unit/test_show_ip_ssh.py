"""Unit tests for show_ip_ssh module command builder."""

from show_ip_ssh import _build_command


def test_show():
    assert _build_command() == "show ip ssh"
