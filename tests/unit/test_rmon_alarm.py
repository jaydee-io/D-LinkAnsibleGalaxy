"""Unit tests for rmon_alarm module command builder."""

from rmon_alarm import _build_commands


def test_full():
    assert _build_commands(783, "1.3.6.1.2.1.2.2.1.12.6", 30, "delta",
                           20, 1, 10, 1, "Name", "present") == [
        "rmon alarm 783 1.3.6.1.2.1.2.2.1.12.6 30 delta rising-threshold 20 1 falling-threshold 10 1 owner Name",
    ]


def test_no_events():
    assert _build_commands(1, "1.3.6.1.2.1.2.2.1.10.1", 120, "absolute",
                           2000, None, 1100, None, None, "present") == [
        "rmon alarm 1 1.3.6.1.2.1.2.2.1.10.1 120 absolute rising-threshold 2000 falling-threshold 1100",
    ]


def test_remove():
    assert _build_commands(783, None, None, None, None, None, None, None, None, "absent") == [
        "no rmon alarm 783",
    ]
