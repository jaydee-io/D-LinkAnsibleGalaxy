"""Unit tests for dns_show_hosts module command builder."""

from dns_show_hosts import _build_command


def test_build_command():
    cmd = _build_command()
    assert cmd == "show hosts"
