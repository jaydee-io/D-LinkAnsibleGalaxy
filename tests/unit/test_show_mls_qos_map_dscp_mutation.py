"""Unit tests for show_mls_qos_map_dscp_mutation module command builder."""

from show_mls_qos_map_dscp_mutation import _build_command


def test_no_name():
    assert _build_command(None) == "show mls qos map dscp-mutation"


def test_with_name():
    assert _build_command("mutemap1") == "show mls qos map dscp-mutation mutemap1"
