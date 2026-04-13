"""Unit tests for impb_clear_violation module."""

from impb_clear_violation import _build_commands


def test_clear_all():
    assert _build_commands("all", None, None) == ["clear ip ip-mac-port-binding violation all"]


def test_clear_interface():
    assert _build_commands("interface", "eth1/0/4", None) == [
        "clear ip ip-mac-port-binding violation interface eth1/0/4"
    ]


def test_clear_mac():
    assert _build_commands("mac_address", None, "01-00-0C-CC-CC-CC") == [
        "clear ip ip-mac-port-binding violation 01-00-0C-CC-CC-CC"
    ]
