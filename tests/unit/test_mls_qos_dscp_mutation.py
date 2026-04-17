"""Unit tests for mls_qos_dscp_mutation module command builder."""

from mls_qos_dscp_mutation import _build_commands


def test_attach():
    assert _build_commands("eth1/0/1", "mutemap1", "present") == [
        "interface eth1/0/1",
        "mls qos dscp-mutation mutemap1",
        "exit",
    ]


def test_remove():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1",
        "no mls qos dscp-mutation",
        "exit",
    ]
