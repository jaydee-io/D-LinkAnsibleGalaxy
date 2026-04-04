"""Unit tests for snmp_environment_traps module command builder."""

from snmp_environment_traps import _build_command


def test_enable_all_traps():
    cmd = _build_command("enabled", False, False, False)
    assert cmd == "snmp-server enable traps environment"


def test_disable_all_traps():
    cmd = _build_command("disabled", False, False, False)
    assert cmd == "no snmp-server enable traps environment"


def test_enable_fan_only():
    cmd = _build_command("enabled", True, False, False)
    assert cmd == "snmp-server enable traps environment fan"


def test_enable_fan_and_temperature():
    cmd = _build_command("enabled", True, False, True)
    assert cmd == "snmp-server enable traps environment fan temperature"


def test_disable_power_only():
    cmd = _build_command("disabled", False, True, False)
    assert cmd == "no snmp-server enable traps environment power"


def test_enable_all_components():
    cmd = _build_command("enabled", True, True, True)
    assert cmd == "snmp-server enable traps environment fan power temperature"
