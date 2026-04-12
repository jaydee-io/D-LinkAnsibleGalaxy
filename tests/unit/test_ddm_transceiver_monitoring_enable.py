"""Unit tests for ddm_transceiver_monitoring_enable module command builder."""

from ddm_transceiver_monitoring_enable import _build_commands


def test_enable():
    cmds = _build_commands("eth1/0/25", "enabled")
    assert cmds == ["interface eth1/0/25", "transceiver-monitoring enable", "exit"]


def test_disable():
    cmds = _build_commands("eth1/0/25", "disabled")
    assert cmds == ["interface eth1/0/25", "no transceiver-monitoring enable", "exit"]
