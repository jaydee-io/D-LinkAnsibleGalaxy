"""Unit tests for dgs1250_ntp resource module."""

from dgs1250_ntp import (
    _parse_sntp_servers,
    _build_commands_merged,
    _build_commands_overridden,
    _build_commands_deleted,
    _have_set,
)


CONFIG = """\
sntp server 0.pool.ntp.org
sntp server 1.pool.ntp.org
"""


def _have():
    return _parse_sntp_servers(CONFIG)


def _addrs():
    return _have_set(_have())


class TestParser:
    def test_parse(self):
        servers = _have()
        addrs = [s["address"] for s in servers]
        assert "0.pool.ntp.org" in addrs
        assert "1.pool.ntp.org" in addrs

    def test_parse_empty(self):
        assert _parse_sntp_servers("") == []


class TestMerged:
    def test_add_new(self):
        want = [{"address": "2.pool.ntp.org"}]
        cmds = _build_commands_merged(want, _addrs())
        assert cmds == ["sntp server 2.pool.ntp.org"]

    def test_no_change(self):
        want = [{"address": "0.pool.ntp.org"}]
        cmds = _build_commands_merged(want, _addrs())
        assert cmds == []


class TestOverridden:
    def test_removes_extra(self):
        want = [{"address": "ntp.company.com"}]
        cmds = _build_commands_overridden(want, _addrs())
        assert "no sntp server 0.pool.ntp.org" in cmds
        assert "no sntp server 1.pool.ntp.org" in cmds
        assert "sntp server ntp.company.com" in cmds

    def test_no_change(self):
        want = [{"address": "0.pool.ntp.org"}, {"address": "1.pool.ntp.org"}]
        cmds = _build_commands_overridden(want, _addrs())
        assert cmds == []


class TestDeleted:
    def test_delete_specific(self):
        want = [{"address": "0.pool.ntp.org"}]
        cmds = _build_commands_deleted(want, _addrs())
        assert cmds == ["no sntp server 0.pool.ntp.org"]

    def test_delete_all(self):
        cmds = _build_commands_deleted([], _addrs())
        assert len(cmds) == 2

    def test_delete_nonexistent(self):
        want = [{"address": "unknown.ntp.org"}]
        cmds = _build_commands_deleted(want, _addrs())
        assert cmds == []
