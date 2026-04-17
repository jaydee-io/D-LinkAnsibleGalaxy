"""Unit tests for mls_qos_cos module command builder."""

from mls_qos_cos import _build_commands


def test_set_cos():
    assert _build_commands("eth1/0/1", 3, False, "present") == [
        "interface eth1/0/1",
        "mls qos cos 3",
        "exit",
    ]


def test_override():
    assert _build_commands("eth1/0/1", None, True, "present") == [
        "interface eth1/0/1",
        "mls qos cos override",
        "exit",
    ]


def test_revert_default():
    assert _build_commands("eth1/0/1", None, False, "absent") == [
        "interface eth1/0/1",
        "no mls qos cos",
        "exit",
    ]
