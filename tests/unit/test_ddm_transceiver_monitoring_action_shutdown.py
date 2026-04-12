"""Unit tests for ddm_transceiver_monitoring_action_shutdown module command builder."""

from ddm_transceiver_monitoring_action_shutdown import _build_commands


def test_shutdown_alarm():
    cmds = _build_commands("eth1/0/25", "alarm", "present")
    assert cmds == ["interface eth1/0/25", "transceiver-monitoring action shutdown alarm", "exit"]


def test_shutdown_warning():
    cmds = _build_commands("eth1/0/25", "warning", "present")
    assert cmds == ["interface eth1/0/25", "transceiver-monitoring action shutdown warning", "exit"]


def test_remove():
    cmds = _build_commands("eth1/0/25", None, "absent")
    assert cmds == ["interface eth1/0/25", "no transceiver-monitoring action shutdown", "exit"]
