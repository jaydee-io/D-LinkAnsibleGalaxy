"""Unit tests for mls_qos_map_dscp_cos module command builder."""

from mls_qos_map_dscp_cos import _build_commands


def test_set_mapping():
    assert _build_commands("eth1/0/6", "12,16,18", 1, "present") == [
        "interface eth1/0/6",
        "mls qos map dscp-cos 12,16,18 to 1",
        "exit",
    ]


def test_remove_mapping():
    assert _build_commands("eth1/0/6", "12,16,18", None, "absent") == [
        "interface eth1/0/6",
        "no mls qos map dscp-cos 12,16,18",
        "exit",
    ]
