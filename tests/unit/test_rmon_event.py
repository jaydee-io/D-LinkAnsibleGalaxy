"""Unit tests for rmon_event module command builder."""

from rmon_event import _build_commands


def test_log_and_owner():
    assert _build_commands(13, True, None, "it@domain.com",
                           "ifInNUcastPkts is too much", "present") == [
        "rmon event 13 log owner it@domain.com description ifInNUcastPkts is too much",
    ]


def test_trap():
    assert _build_commands(1, False, "manager", "mgr1", "Errors", "present") == [
        "rmon event 1 trap manager owner mgr1 description Errors",
    ]


def test_log_and_trap():
    assert _build_commands(2, True, "manager", "mgr2", "Errors", "present") == [
        "rmon event 2 log trap manager owner mgr2 description Errors",
    ]


def test_remove():
    assert _build_commands(13, False, None, None, None, "absent") == [
        "no rmon event 13",
    ]
