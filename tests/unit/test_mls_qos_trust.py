"""Unit tests for mls_qos_trust module command builder."""

from mls_qos_trust import _build_commands


def test_trust_dscp():
    assert _build_commands("eth1/0/1", "dscp", "present") == [
        "interface eth1/0/1",
        "mls qos trust dscp",
        "exit",
    ]


def test_trust_cos():
    assert _build_commands("eth1/0/1", "cos", "present") == [
        "interface eth1/0/1",
        "mls qos trust cos",
        "exit",
    ]


def test_revert():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1",
        "no mls qos trust",
        "exit",
    ]
