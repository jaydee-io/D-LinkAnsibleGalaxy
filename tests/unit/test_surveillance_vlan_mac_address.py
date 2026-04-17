"""Unit tests for surveillance_vlan_mac_address module."""

from surveillance_vlan_mac_address import _build_commands


def test_add_with_type_and_desc():
    assert _build_commands("00-01-02-03-00-00", "FF-FF-FF-FF-00-00", "vms", "user1", "present") == [
        "surveillance vlan mac-address 00-01-02-03-00-00 FF-FF-FF-FF-00-00 component-type vms description user1"]


def test_add_simple():
    assert _build_commands("00-01-02-03-00-00", "FF-FF-FF-FF-00-00", None, None, "present") == [
        "surveillance vlan mac-address 00-01-02-03-00-00 FF-FF-FF-FF-00-00"]


def test_remove():
    assert _build_commands("00-01-02-03-00-00", "FF-FF-FF-FF-00-00", None, None, "absent") == [
        "no surveillance vlan mac-address 00-01-02-03-00-00 FF-FF-FF-FF-00-00"]
