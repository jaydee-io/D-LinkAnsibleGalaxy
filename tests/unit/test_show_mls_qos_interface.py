"""Unit tests for show_mls_qos_interface module command builder."""

from show_mls_qos_interface import _build_command


def test_cos():
    assert _build_command("eth1/0/2-5", "cos") == \
        "show mls qos interface eth1/0/2-5 cos"


def test_scheduler():
    assert _build_command("eth1/0/1-2", "scheduler") == \
        "show mls qos interface eth1/0/1-2 scheduler"


def test_map_dscp_cos():
    assert _build_command("eth1/0/1", "map-dscp-cos") == \
        "show mls qos interface eth1/0/1 map dscp-cos"
