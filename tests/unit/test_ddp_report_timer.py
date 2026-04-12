"""Unit tests for ddp_report_timer module command builder."""

from ddp_report_timer import _build_commands


def test_set_60():
    cmds = _build_commands("60", "present")
    assert cmds == ["ddp report-timer 60"]


def test_set_never():
    cmds = _build_commands("never", "present")
    assert cmds == ["ddp report-timer never"]


def test_remove():
    cmds = _build_commands(None, "absent")
    assert cmds == ["no ddp report-timer"]
