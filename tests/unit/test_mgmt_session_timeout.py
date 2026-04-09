"""Unit tests for mgmt_session_timeout module command builder."""

from mgmt_session_timeout import _build_commands


def test_set_timeout():
    assert _build_commands("telnet", 30, "present") == [
        "line telnet",
        "session-timeout 30",
        "exit",
    ]


def test_remove_timeout():
    assert _build_commands("ssh", None, "absent") == [
        "line ssh",
        "no session-timeout",
        "exit",
    ]


def test_console_timeout():
    assert _build_commands("console", 10, "present") == [
        "line console",
        "session-timeout 10",
        "exit",
    ]
