"""Unit tests for auth_host_mode module command builder."""

from auth_host_mode import _build_commands


def test_multi_host():
    assert _build_commands("eth1/0/1", "multi-host", "present") == [
        "interface eth1/0/1",
        "authentication host-mode multi-host",
        "exit",
    ]


def test_multi_auth():
    assert _build_commands("eth1/0/1", "multi-auth", "present") == [
        "interface eth1/0/1",
        "authentication host-mode multi-auth",
        "exit",
    ]


def test_absent():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1",
        "no authentication host-mode",
        "exit",
    ]
