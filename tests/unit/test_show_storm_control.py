"""Unit tests for show_storm_control module."""

from show_storm_control import _build_command


def test_all_types():
    assert _build_command("eth1/0/1-6", None) == "show storm-control interface eth1/0/1-6"


def test_broadcast():
    assert _build_command("eth1/0/1-6", "broadcast") == "show storm-control interface eth1/0/1-6 broadcast"
