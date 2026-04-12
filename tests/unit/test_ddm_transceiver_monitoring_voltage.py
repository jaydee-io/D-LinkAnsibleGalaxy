"""Unit tests for ddm_transceiver_monitoring_voltage module command builder."""

from ddm_transceiver_monitoring_voltage import _build_commands


def test_set_low_alarm():
    cmds = _build_commands("eth1/0/25", "low", "alarm", 0.005, "present")
    assert cmds == ["transceiver-monitoring voltage eth1/0/25 low alarm 0.005"]


def test_set_high_warning():
    cmds = _build_commands("eth1/0/25", "high", "warning", 3.6, "present")
    assert cmds == ["transceiver-monitoring voltage eth1/0/25 high warning 3.6"]


def test_remove():
    cmds = _build_commands("eth1/0/25", "low", "alarm", None, "absent")
    assert cmds == ["no transceiver-monitoring voltage eth1/0/25 low alarm"]
