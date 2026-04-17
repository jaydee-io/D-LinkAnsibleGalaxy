"""Unit tests for mls_qos_scheduler module command builder."""

from mls_qos_scheduler import _build_commands


def test_sp():
    assert _build_commands("eth1/0/1", "sp", "present") == [
        "interface eth1/0/1",
        "mls qos scheduler sp",
        "exit",
    ]


def test_wdrr():
    assert _build_commands("eth1/0/2", "wdrr", "present") == [
        "interface eth1/0/2",
        "mls qos scheduler wdrr",
        "exit",
    ]


def test_revert():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1",
        "no mls qos scheduler",
        "exit",
    ]
