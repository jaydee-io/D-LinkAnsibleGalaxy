"""Unit tests for mstp_name module command builder."""

from mstp_name import _build_commands


def test_set_name():
    assert _build_commands("MName", "present") == [
        "spanning-tree mst configuration",
        "name MName",
        "exit",
    ]


def test_reset_name():
    assert _build_commands(None, "absent") == [
        "spanning-tree mst configuration",
        "no name",
        "exit",
    ]
