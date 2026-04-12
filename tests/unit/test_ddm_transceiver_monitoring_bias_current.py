"""Unit tests for ddm_transceiver_monitoring_bias_current module command builder."""

from ddm_transceiver_monitoring_bias_current import _build_commands


def test_set_high_warning():
    cmds = _build_commands("eth1/0/25", "high", "warning", 10.237, "present")
    assert cmds == ["transceiver-monitoring bias-current eth1/0/25 high warning 10.237"]


def test_set_low_alarm():
    cmds = _build_commands("eth1/0/25", "low", "alarm", 4.0, "present")
    assert cmds == ["transceiver-monitoring bias-current eth1/0/25 low alarm 4.0"]


def test_remove():
    cmds = _build_commands("eth1/0/25", "high", "warning", None, "absent")
    assert cmds == ["no transceiver-monitoring bias-current eth1/0/25 high warning"]
