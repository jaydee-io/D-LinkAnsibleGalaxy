"""Unit tests for show_mac_address_table module."""

from show_mac_address_table import _build_command


def test_show_all():
    assert _build_command(None, None, None, None) == "show mac-address-table"


def test_show_static():
    assert _build_command("static", None, None, None) == "show mac-address-table static"


def test_show_dynamic():
    assert _build_command("dynamic", None, None, None) == "show mac-address-table dynamic"


def test_show_address():
    assert _build_command(None, "00:02:4B:28:C4:82", None, None) == (
        "show mac-address-table address 00:02:4B:28:C4:82"
    )


def test_show_vlan():
    assert _build_command(None, None, None, 1) == "show mac-address-table vlan 1"


def test_show_interface():
    assert _build_command(None, None, "eth1/0/1", None) == "show mac-address-table interface eth1/0/1"
