"""Unit tests for lldp_dot3_tlv_select module."""

from lldp_dot3_tlv_select import _build_commands


def test_enable_mac_phy_cfg():
    assert _build_commands("eth1/0/1", "mac-phy-cfg", "enabled") == [
        "interface eth1/0/1", "lldp dot3-tlv-select mac-phy-cfg", "exit"]


def test_disable_power():
    assert _build_commands("eth1/0/1", "power", "disabled") == [
        "interface eth1/0/1", "no lldp dot3-tlv-select power", "exit"]


def test_enable_all():
    assert _build_commands("eth1/0/1", None, "enabled") == [
        "interface eth1/0/1", "lldp dot3-tlv-select", "exit"]
