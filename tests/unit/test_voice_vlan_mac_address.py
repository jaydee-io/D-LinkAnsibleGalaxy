"""Unit tests for voice_vlan_mac_address module."""

from voice_vlan_mac_address import _build_commands


def test_add_with_description():
    assert _build_commands("00-02-03-00-00-00", "FF-FF-FF-00-00-00", "User1", "present") == [
        "voice vlan mac-address 00-02-03-00-00-00 FF-FF-FF-00-00-00 description User1"]


def test_add_simple():
    assert _build_commands("00-02-03-00-00-00", "FF-FF-FF-00-00-00", None, "present") == [
        "voice vlan mac-address 00-02-03-00-00-00 FF-FF-FF-00-00-00"]


def test_remove():
    assert _build_commands("00-02-03-00-00-00", "FF-FF-FF-00-00-00", None, "absent") == [
        "no voice vlan mac-address 00-02-03-00-00-00 FF-FF-FF-00-00-00"]
