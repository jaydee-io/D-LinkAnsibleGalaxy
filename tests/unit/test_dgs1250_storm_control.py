"""Unit tests for dgs1250_storm_control resource module."""

from dgs1250_storm_control import (
    _parse_storm_control,
    _build_commands_merged,
    _build_commands_replaced,
    _build_commands_deleted,
    _index_by_name,
)


CONFIG = """\
interface eth1/0/1
 storm-control broadcast level 80
 storm-control multicast level 70
 storm-control action shutdown
!
interface eth1/0/2
 storm-control broadcast level 50
!
"""


def _have():
    return _parse_storm_control(CONFIG)


def _have_idx():
    return _index_by_name(_have())


class TestParser:
    def test_parse_full(self):
        idx = _have_idx()
        assert idx["eth1/0/1"]["broadcast"] == 80
        assert idx["eth1/0/1"]["multicast"] == 70
        assert idx["eth1/0/1"]["action"] == "shutdown"

    def test_parse_partial(self):
        idx = _have_idx()
        assert idx["eth1/0/2"]["broadcast"] == 50
        assert "multicast" not in idx["eth1/0/2"]

    def test_parse_empty(self):
        assert _parse_storm_control("") == []


class TestMerged:
    def test_add_new(self):
        want = [{"name": "eth1/0/3", "broadcast": 90}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "interface eth1/0/3" in cmds
        assert "storm-control broadcast level 90" in cmds

    def test_no_change(self):
        want = [{"name": "eth1/0/1", "broadcast": 80}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == []

    def test_change_level(self):
        want = [{"name": "eth1/0/1", "broadcast": 90}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "storm-control broadcast level 90" in cmds


class TestReplaced:
    def test_replace_removes_extra(self):
        want = [{"name": "eth1/0/1", "broadcast": 80}]
        cmds = _build_commands_replaced(want, _have_idx())
        assert "no storm-control multicast" in cmds
        assert "no storm-control action" in cmds

    def test_replace_no_change(self):
        want = [{"name": "eth1/0/1", "broadcast": 80, "multicast": 70, "action": "shutdown"}]
        cmds = _build_commands_replaced(want, _have_idx())
        assert cmds == []


class TestDeleted:
    def test_delete_specific(self):
        want = [{"name": "eth1/0/1"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert "no storm-control broadcast" in cmds
        assert "no storm-control multicast" in cmds
        assert "no storm-control action" in cmds

    def test_delete_all(self):
        cmds = _build_commands_deleted([], _have_idx())
        assert "interface eth1/0/1" in cmds
        assert "interface eth1/0/2" in cmds

    def test_delete_nonexistent(self):
        want = [{"name": "eth1/0/99"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == []
