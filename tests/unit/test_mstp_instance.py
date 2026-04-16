"""Unit tests for mstp_instance module command builder."""

from mstp_instance import _build_commands


def test_map_vlans():
    assert _build_commands(2, "1-100", "present") == [
        "spanning-tree mst configuration",
        "instance 2 vlans 1-100",
        "exit",
    ]


def test_remove_instance():
    assert _build_commands(2, None, "absent") == [
        "spanning-tree mst configuration",
        "no instance 2",
        "exit",
    ]
