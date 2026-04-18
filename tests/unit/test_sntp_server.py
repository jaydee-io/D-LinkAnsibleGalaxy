"""Unit tests for sntp_server module."""

from sntp_server import _build_commands


def test_add():
    assert _build_commands("192.168.22.44", "present") == ["sntp server 192.168.22.44"]


def test_remove():
    assert _build_commands("192.168.22.44", "absent") == ["no sntp server 192.168.22.44"]
