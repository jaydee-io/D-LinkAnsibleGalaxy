"""Unit tests for mac_auth_enable module."""

from mac_auth_enable import _build_commands


def test_enable():
    assert _build_commands("eth1/0/1", "enabled") == [
        "interface eth1/0/1", "mac-auth enable", "exit"]


def test_disable():
    assert _build_commands("eth1/0/1", "disabled") == [
        "interface eth1/0/1", "no mac-auth enable", "exit"]
