"""Unit tests for mstp_hello_time module command builder."""

from mstp_hello_time import _build_commands


def test_set_hello_time():
    assert _build_commands("eth1/0/1", 1, "present") == [
        "interface eth1/0/1",
        "spanning-tree mst hello-time 1",
        "exit",
    ]


def test_reset_hello_time():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1",
        "no spanning-tree mst hello-time",
        "exit",
    ]
