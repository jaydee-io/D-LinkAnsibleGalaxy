"""Unit tests for ddm_snmp_traps_transceiver_monitoring module command builder."""

from ddm_snmp_traps_transceiver_monitoring import _build_commands


def test_enable_all():
    cmds = _build_commands(None, "enabled")
    assert cmds == ["snmp-server enable traps transceiver-monitoring"]


def test_enable_alarm():
    cmds = _build_commands("alarm", "enabled")
    assert cmds == ["snmp-server enable traps transceiver-monitoring alarm"]


def test_enable_warning():
    cmds = _build_commands("warning", "enabled")
    assert cmds == ["snmp-server enable traps transceiver-monitoring warning"]


def test_disable_all():
    cmds = _build_commands(None, "disabled")
    assert cmds == ["no snmp-server enable traps transceiver-monitoring"]


def test_disable_alarm():
    cmds = _build_commands("alarm", "disabled")
    assert cmds == ["no snmp-server enable traps transceiver-monitoring alarm"]
