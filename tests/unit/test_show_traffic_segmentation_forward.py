"""Unit tests for show_traffic_segmentation_forward module."""

from show_traffic_segmentation_forward import _build_command


def test_all():
    assert _build_command(None) == "show traffic-segmentation forward"


def test_interface():
    assert _build_command("eth1/0/1") == "show traffic-segmentation forward interface eth1/0/1"
