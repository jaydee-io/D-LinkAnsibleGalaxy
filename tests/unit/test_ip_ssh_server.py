"""Unit tests for ip_ssh_server module command builder."""

from ip_ssh_server import _build_commands


def test_enable():
    assert _build_commands("enabled") == [
        "ip ssh server",
    ]


def test_disable():
    assert _build_commands("disabled") == [
        "no ip ssh server",
    ]
