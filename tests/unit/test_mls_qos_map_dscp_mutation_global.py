"""Unit tests for mls_qos_map_dscp_mutation_global module command builder."""

from mls_qos_map_dscp_mutation_global import _build_commands


def test_add_mapping():
    assert _build_commands("mutemap1", "30", 8, "present") == [
        "mls qos map dscp-mutation mutemap1 30 to 8",
    ]


def test_add_mapping_list():
    assert _build_commands("mutemap1", "20,30", 10, "present") == [
        "mls qos map dscp-mutation mutemap1 20,30 to 10",
    ]


def test_remove():
    assert _build_commands("mutemap1", None, None, "absent") == [
        "no mls qos map dscp-mutation mutemap1",
    ]
