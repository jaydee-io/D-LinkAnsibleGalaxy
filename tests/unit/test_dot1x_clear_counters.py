"""Unit tests for dot1x_clear_counters module command builder."""

from dot1x_clear_counters import _build_commands


def test_clear_all():
    cmds = _build_commands(None)
    assert cmds == ["clear dot1x counters all"]


def test_clear_all_empty_list():
    cmds = _build_commands([])
    assert cmds == ["clear dot1x counters all"]


def test_clear_single_interface():
    cmds = _build_commands(["eth1/0/1"])
    assert cmds == ["clear dot1x counters interface eth1/0/1"]


def test_clear_multiple_interfaces():
    cmds = _build_commands(["eth1/0/1", "eth1/0/5"])
    assert cmds == [
        "clear dot1x counters interface eth1/0/1",
        "clear dot1x counters interface eth1/0/5",
    ]


def test_clear_range():
    cmds = _build_commands(["eth1/0/1-eth1/0/8"])
    assert cmds == ["clear dot1x counters interface eth1/0/1-eth1/0/8"]
