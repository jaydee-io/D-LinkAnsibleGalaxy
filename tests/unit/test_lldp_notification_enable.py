"""Unit tests for lldp_notification_enable module."""

from lldp_notification_enable import _build_commands


def test_enable_lldp():
    assert _build_commands("eth1/0/1", False, "enabled") == [
        "interface eth1/0/1", "lldp notification enable", "exit"]


def test_enable_med():
    assert _build_commands("eth1/0/1", True, "enabled") == [
        "interface eth1/0/1", "lldp med notification enable", "exit"]


def test_disable_lldp():
    assert _build_commands("eth1/0/1", False, "disabled") == [
        "interface eth1/0/1", "no lldp notification enable", "exit"]
