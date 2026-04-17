"""Unit tests for rate_limit module command builder."""

from rate_limit import _build_commands


def test_input_kbps_burst():
    assert _build_commands("eth1/0/5", "input", 2000, None, 30, "present") == [
        "interface eth1/0/5",
        "rate-limit input 2000 30",
        "exit",
    ]


def test_output_percent():
    assert _build_commands("eth1/0/5", "output", None, 10, None, "present") == [
        "interface eth1/0/5",
        "rate-limit output percent 10",
        "exit",
    ]


def test_remove():
    assert _build_commands("eth1/0/5", "input", None, None, None, "absent") == [
        "interface eth1/0/5",
        "no rate-limit input",
        "exit",
    ]
