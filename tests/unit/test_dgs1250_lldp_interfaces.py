"""Unit tests for dgs1250_lldp_interfaces resource module."""

from dgs1250_lldp_interfaces import (
    _parse_lldp_interfaces,
    _build_commands_merged,
    _build_commands_deleted,
    _index_by_name,
)


CONFIG = """\
interface eth1/0/1
 no lldp transmit
 no lldp receive
!
interface eth1/0/2
 no lldp transmit
!
"""


def _have():
    return _parse_lldp_interfaces(CONFIG)


def _have_idx():
    return _index_by_name(_have())


class TestParser:
    def test_parse_both_disabled(self):
        idx = _have_idx()
        assert idx["eth1/0/1"]["transmit"] is False
        assert idx["eth1/0/1"]["receive"] is False

    def test_parse_transmit_only(self):
        idx = _have_idx()
        assert idx["eth1/0/2"]["transmit"] is False
        assert idx["eth1/0/2"]["receive"] is True

    def test_parse_empty(self):
        assert _parse_lldp_interfaces("") == []


class TestMerged:
    def test_disable_lldp(self):
        want = [{"name": "eth1/0/5", "transmit": False, "receive": False}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "interface eth1/0/5" in cmds
        assert "no lldp transmit" in cmds
        assert "no lldp receive" in cmds

    def test_no_change(self):
        want = [{"name": "eth1/0/1", "transmit": False, "receive": False}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == []

    def test_re_enable_transmit(self):
        want = [{"name": "eth1/0/1", "transmit": True}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "lldp transmit" in cmds

    def test_default_port_no_change(self):
        want = [{"name": "eth1/0/10", "transmit": True, "receive": True}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == []


class TestDeleted:
    def test_delete_restores_defaults(self):
        want = [{"name": "eth1/0/1"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert "lldp transmit" in cmds
        assert "lldp receive" in cmds

    def test_delete_partial(self):
        want = [{"name": "eth1/0/2"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert "lldp transmit" in cmds
        assert "lldp receive" not in cmds

    def test_delete_all(self):
        cmds = _build_commands_deleted([], _have_idx())
        assert "interface eth1/0/1" in cmds
        assert "interface eth1/0/2" in cmds

    def test_delete_nonexistent(self):
        want = [{"name": "eth1/0/99"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == []
