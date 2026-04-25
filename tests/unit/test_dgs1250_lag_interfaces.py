"""Unit tests for dgs1250_lag_interfaces resource module."""

from dgs1250_lag_interfaces import (
    _parse_lag_interfaces,
    _build_commands_merged,
    _build_commands_deleted,
    _index_by_name,
)


CONFIG = """\
interface eth1/0/1
 channel-group 1 mode active
!
interface eth1/0/2
 channel-group 1 mode active
!
interface eth1/0/5
 channel-group 2 mode on
!
"""


def _have():
    return _parse_lag_interfaces(CONFIG)


def _have_idx():
    return _index_by_name(_have())


class TestParser:
    def test_parse_members(self):
        members = _have()
        assert len(members) == 3
        idx = _have_idx()
        assert idx["eth1/0/1"]["channel_group"] == 1
        assert idx["eth1/0/1"]["mode"] == "active"
        assert idx["eth1/0/5"]["channel_group"] == 2
        assert idx["eth1/0/5"]["mode"] == "on"

    def test_parse_empty(self):
        assert _parse_lag_interfaces("") == []


class TestMerged:
    def test_add_new_member(self):
        want = [{"name": "eth1/0/3", "channel_group": 1, "mode": "active"}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "interface eth1/0/3" in cmds
        assert "channel-group 1 mode active" in cmds

    def test_no_change(self):
        want = [{"name": "eth1/0/1", "channel_group": 1, "mode": "active"}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == []

    def test_change_mode(self):
        want = [{"name": "eth1/0/1", "channel_group": 1, "mode": "passive"}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "channel-group 1 mode passive" in cmds

    def test_change_group(self):
        want = [{"name": "eth1/0/5", "channel_group": 3, "mode": "on"}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "channel-group 3 mode on" in cmds


class TestDeleted:
    def test_delete_specific(self):
        want = [{"name": "eth1/0/1"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert "interface eth1/0/1" in cmds
        assert "no channel-group" in cmds

    def test_delete_all(self):
        cmds = _build_commands_deleted([], _have_idx())
        assert len([c for c in cmds if c == "no channel-group"]) == 3

    def test_delete_nonexistent(self):
        want = [{"name": "eth1/0/99"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == []
