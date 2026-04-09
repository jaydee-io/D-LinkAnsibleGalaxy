"""Unit tests for aaa_clear_counters_servers module command builder."""

from aaa_clear_counters_servers import _build_commands


def test_all():
    cmds = _build_commands("all", None)
    assert cmds == ["clear aaa counters servers all"]


def test_radius_with_ip():
    cmds = _build_commands("radius", "1.2.3.4")
    assert cmds == ["clear aaa counters servers radius 1.2.3.4"]


def test_sg_with_name():
    cmds = _build_commands("sg", "my_group")
    assert cmds == ["clear aaa counters servers sg my_group"]
