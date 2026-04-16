"""Unit tests for mstp_revision module command builder."""

from mstp_revision import _build_commands


def test_set_revision():
    assert _build_commands(2, "present") == [
        "spanning-tree mst configuration",
        "revision 2",
        "exit",
    ]


def test_reset_revision():
    assert _build_commands(None, "absent") == [
        "spanning-tree mst configuration",
        "no revision",
        "exit",
    ]
