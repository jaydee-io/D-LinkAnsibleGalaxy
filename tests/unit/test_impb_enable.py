"""Unit tests for impb_enable module."""

from impb_enable import _build_commands


def test_enable_strict():
    assert _build_commands("eth1/0/10", "strict-mode", "enabled") == [
        "interface eth1/0/10",
        "ip ip-mac-port-binding strict-mode",
        "exit",
    ]


def test_enable_loose():
    assert _build_commands("eth1/0/10", "loose-mode", "enabled") == [
        "interface eth1/0/10",
        "ip ip-mac-port-binding loose-mode",
        "exit",
    ]


def test_enable_no_mode():
    assert _build_commands("eth1/0/10", None, "enabled") == [
        "interface eth1/0/10",
        "ip ip-mac-port-binding",
        "exit",
    ]


def test_disabled():
    assert _build_commands("eth1/0/10", None, "disabled") == [
        "interface eth1/0/10",
        "no ip ip-mac-port-binding",
        "exit",
    ]
