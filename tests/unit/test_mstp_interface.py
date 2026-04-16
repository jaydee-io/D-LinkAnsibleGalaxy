"""Unit tests for mstp_interface module command builder."""

from mstp_interface import _build_commands


def test_set_cost():
    assert _build_commands("eth1/0/1", 0, 17031970, None, "present") == [
        "interface eth1/0/1",
        "spanning-tree mst 0 cost 17031970",
        "exit",
    ]


def test_set_port_priority():
    assert _build_commands("eth1/0/1", 0, None, 64, "present") == [
        "interface eth1/0/1",
        "spanning-tree mst 0 port-priority 64",
        "exit",
    ]


def test_reset_cost():
    assert _build_commands("eth1/0/1", 0, 1, None, "absent") == [
        "interface eth1/0/1",
        "no spanning-tree mst 0 cost",
        "exit",
    ]


def test_reset_port_priority():
    assert _build_commands("eth1/0/1", 0, None, 64, "absent") == [
        "interface eth1/0/1",
        "no spanning-tree mst 0 port-priority",
        "exit",
    ]
