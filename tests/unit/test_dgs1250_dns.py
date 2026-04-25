"""Unit tests for dgs1250_dns resource module."""

from dgs1250_dns import (
    _parse_dns_servers,
    _build_commands_merged,
    _build_commands_overridden,
    _build_commands_deleted,
    _have_set,
)


CONFIG = """\
ip name-server 8.8.8.8
ip name-server 8.8.4.4
"""


def _have():
    return _parse_dns_servers(CONFIG)


def _addrs():
    return _have_set(_have())


class TestParser:
    def test_parse(self):
        servers = _have()
        addrs = [s["address"] for s in servers]
        assert "8.8.8.8" in addrs
        assert "8.8.4.4" in addrs

    def test_parse_empty(self):
        assert _parse_dns_servers("") == []


class TestMerged:
    def test_add_new(self):
        want = [{"address": "1.1.1.1"}]
        cmds = _build_commands_merged(want, _addrs())
        assert cmds == ["ip name-server 1.1.1.1"]

    def test_no_change(self):
        want = [{"address": "8.8.8.8"}]
        cmds = _build_commands_merged(want, _addrs())
        assert cmds == []


class TestOverridden:
    def test_removes_extra(self):
        want = [{"address": "1.1.1.1"}]
        cmds = _build_commands_overridden(want, _addrs())
        assert "no ip name-server 8.8.4.4" in cmds
        assert "no ip name-server 8.8.8.8" in cmds
        assert "ip name-server 1.1.1.1" in cmds

    def test_no_change(self):
        want = [{"address": "8.8.8.8"}, {"address": "8.8.4.4"}]
        cmds = _build_commands_overridden(want, _addrs())
        assert cmds == []


class TestDeleted:
    def test_delete_specific(self):
        want = [{"address": "8.8.4.4"}]
        cmds = _build_commands_deleted(want, _addrs())
        assert cmds == ["no ip name-server 8.8.4.4"]

    def test_delete_all(self):
        cmds = _build_commands_deleted([], _addrs())
        assert len(cmds) == 2

    def test_delete_nonexistent(self):
        want = [{"address": "9.9.9.9"}]
        cmds = _build_commands_deleted(want, _addrs())
        assert cmds == []
