"""Unit tests for ddm_transceiver_monitoring_rx_power module command builder."""

from ddm_transceiver_monitoring_rx_power import _build_commands


def test_set_mwatt():
    cmds = _build_commands("eth1/0/25", "low", "warning", "mwatt", 0.135, "present")
    assert cmds == ["transceiver-monitoring rx-power eth1/0/25 low warning mwatt 0.135"]


def test_set_dbm():
    cmds = _build_commands("eth1/0/25", "high", "alarm", "dbm", 0.0, "present")
    assert cmds == ["transceiver-monitoring rx-power eth1/0/25 high alarm dbm 0.0"]


def test_remove():
    cmds = _build_commands("eth1/0/25", "low", "warning", None, None, "absent")
    assert cmds == ["no transceiver-monitoring rx-power eth1/0/25 low warning"]
