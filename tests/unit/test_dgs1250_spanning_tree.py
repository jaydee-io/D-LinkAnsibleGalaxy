"""Unit tests for dgs1250_spanning_tree resource module."""

from dgs1250_spanning_tree import (
    _parse_stp_interfaces,
    _build_commands_merged,
    _build_commands_replaced,
    _build_commands_deleted,
    _index_by_name,
)


CONFIG = """\
interface eth1/0/1
 spanning-tree portfast
 spanning-tree cost 20000
!
interface eth1/0/24
 spanning-tree guard root
 spanning-tree port-priority 32
!
"""


def _have():
    return _parse_stp_interfaces(CONFIG)


def _have_idx():
    return _index_by_name(_have())


class TestParser:
    def test_parse_portfast_cost(self):
        idx = _have_idx()
        assert idx["eth1/0/1"]["portfast"] is True
        assert idx["eth1/0/1"]["cost"] == 20000

    def test_parse_guard_priority(self):
        idx = _have_idx()
        assert idx["eth1/0/24"]["guard_root"] is True
        assert idx["eth1/0/24"]["port_priority"] == 32

    def test_parse_empty(self):
        assert _parse_stp_interfaces("") == []


class TestMerged:
    def test_add_portfast(self):
        want = [{"name": "eth1/0/5", "portfast": True}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "interface eth1/0/5" in cmds
        assert "spanning-tree portfast" in cmds

    def test_no_change(self):
        want = [{"name": "eth1/0/1", "portfast": True, "cost": 20000}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == []

    def test_change_cost(self):
        want = [{"name": "eth1/0/1", "cost": 10000}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "spanning-tree cost 10000" in cmds

    def test_disable_portfast(self):
        want = [{"name": "eth1/0/1", "portfast": False}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "no spanning-tree portfast" in cmds


class TestReplaced:
    def test_replace_removes_extra(self):
        want = [{"name": "eth1/0/1", "portfast": True}]
        cmds = _build_commands_replaced(want, _have_idx())
        assert "no spanning-tree cost" in cmds

    def test_replace_no_change(self):
        want = [{"name": "eth1/0/1", "portfast": True, "cost": 20000}]
        cmds = _build_commands_replaced(want, _have_idx())
        assert cmds == []


class TestDeleted:
    def test_delete_specific(self):
        want = [{"name": "eth1/0/1"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert "no spanning-tree portfast" in cmds
        assert "no spanning-tree cost" in cmds

    def test_delete_all(self):
        cmds = _build_commands_deleted([], _have_idx())
        assert "interface eth1/0/1" in cmds
        assert "interface eth1/0/24" in cmds

    def test_delete_nonexistent(self):
        want = [{"name": "eth1/0/99"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == []
