"""Unit tests for traffic_segmentation_forward module."""

from traffic_segmentation_forward import _build_commands


def test_add():
    assert _build_commands("eth1/0/1", "eth1/0/3-6", "present") == [
        "interface eth1/0/1", "traffic-segmentation forward interface eth1/0/3-6", "exit"]


def test_remove():
    assert _build_commands("eth1/0/1", "eth1/0/3-6", "absent") == [
        "interface eth1/0/1", "no traffic-segmentation forward interface eth1/0/3-6", "exit"]
