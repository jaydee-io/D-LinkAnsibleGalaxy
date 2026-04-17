"""Unit tests for show_poe_power_inline module command builder."""

from show_poe_power_inline import _build_command


def test_status_all():
    assert _build_command(None, "status") == "show poe power-inline status"


def test_config_interface():
    assert _build_command("eth1/0/1", "configuration") == "show poe power-inline eth1/0/1 configuration"


def test_measurement():
    assert _build_command(None, "measurement") == "show poe power-inline measurement"


def test_lldp():
    assert _build_command("eth1/0/1-3", "lldp-classification") == "show poe power-inline eth1/0/1-3 lldp-classification"
