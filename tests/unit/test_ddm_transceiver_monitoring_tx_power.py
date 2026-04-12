"""Unit tests for ddm_transceiver_monitoring_tx_power module command builder."""

from ddm_transceiver_monitoring_tx_power import _build_commands


def test_set_mwatt():
    cmds = _build_commands("eth1/0/25", "low", "warning", "mwatt", 0.181, "present")
    assert cmds == ["transceiver-monitoring tx-power eth1/0/25 low warning mwatt 0.181"]


def test_set_dbm():
    cmds = _build_commands("eth1/0/25", "high", "alarm", "dbm", -0.8, "present")
    assert cmds == ["transceiver-monitoring tx-power eth1/0/25 high alarm dbm -0.8"]


def test_remove():
    cmds = _build_commands("eth1/0/25", "low", "warning", None, None, "absent")
    assert cmds == ["no transceiver-monitoring tx-power eth1/0/25 low warning"]
