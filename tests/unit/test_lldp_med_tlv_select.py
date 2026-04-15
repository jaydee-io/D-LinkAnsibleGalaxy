"""Unit tests for lldp_med_tlv_select module."""

from lldp_med_tlv_select import _build_commands


def test_enable_capabilities():
    assert _build_commands("eth1/0/1", "capabilities", "enabled") == [
        "interface eth1/0/1", "lldp med-tlv-select capabilities", "exit"]


def test_disable_all():
    assert _build_commands("eth1/0/1", None, "disabled") == [
        "interface eth1/0/1", "no lldp med-tlv-select", "exit"]
