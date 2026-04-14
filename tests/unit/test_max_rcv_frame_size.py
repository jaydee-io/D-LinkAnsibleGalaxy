"""Unit tests for max_rcv_frame_size module."""

from max_rcv_frame_size import _build_commands


def test_present():
    assert _build_commands("eth1/0/3", 6000, "present") == [
        "interface eth1/0/3",
        "max-rcv-frame-size 6000",
        "exit",
    ]


def test_absent():
    assert _build_commands("eth1/0/3", None, "absent") == [
        "interface eth1/0/3",
        "no max-rcv-frame-size",
        "exit",
    ]
