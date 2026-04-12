"""Unit tests for ddm_transceiver_monitoring_temperature module command builder."""

from ddm_transceiver_monitoring_temperature import _build_commands


def test_set_high_alarm():
    cmds = _build_commands("eth1/0/25", "high", "alarm", 127.994, "present")
    assert cmds == ["transceiver-monitoring temperature eth1/0/25 high alarm 127.994"]


def test_set_low_warning():
    cmds = _build_commands("eth1/0/25", "low", "warning", -8.0, "present")
    assert cmds == ["transceiver-monitoring temperature eth1/0/25 low warning -8.0"]


def test_remove():
    cmds = _build_commands("eth1/0/25", "high", "alarm", None, "absent")
    assert cmds == ["no transceiver-monitoring temperature eth1/0/25 high alarm"]
