"""Unit tests for dgs1250_snmp_server resource module."""

from dgs1250_snmp_server import (
    _parse_snmp_communities,
    _build_commands_merged,
    _build_commands_overridden,
    _build_commands_deleted,
    _index_by_name,
)


CONFIG = """\
snmp-server community public ro
snmp-server community private view allView rw
"""


def _have():
    return _parse_snmp_communities(CONFIG)


def _have_idx():
    return _index_by_name(_have())


class TestParser:
    def test_parse_ro(self):
        idx = _have_idx()
        assert idx["public"]["access_type"] == "ro"
        assert idx["public"]["view"] == ""

    def test_parse_rw_with_view(self):
        idx = _have_idx()
        assert idx["private"]["access_type"] == "rw"
        assert idx["private"]["view"] == "allView"

    def test_parse_empty(self):
        assert _parse_snmp_communities("") == []


class TestMerged:
    def test_add_new(self):
        want = [{"community": "monitor", "access_type": "ro", "view": ""}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "snmp-server community monitor ro" in cmds

    def test_no_change(self):
        want = [{"community": "public", "access_type": "ro", "view": ""}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == []

    def test_change_access(self):
        want = [{"community": "public", "access_type": "rw", "view": ""}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "snmp-server community public rw" in cmds


class TestOverridden:
    def test_removes_extra(self):
        want = [{"community": "public", "access_type": "ro", "view": ""}]
        cmds = _build_commands_overridden(want, _have_idx())
        assert "no snmp-server community private" in cmds

    def test_no_change(self):
        want = [
            {"community": "public", "access_type": "ro", "view": ""},
            {"community": "private", "access_type": "rw", "view": "allView"},
        ]
        cmds = _build_commands_overridden(want, _have_idx())
        assert cmds == []


class TestDeleted:
    def test_delete_specific(self):
        want = [{"community": "public"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == ["no snmp-server community public"]

    def test_delete_all(self):
        cmds = _build_commands_deleted([], _have_idx())
        assert "no snmp-server community public" in cmds
        assert "no snmp-server community private" in cmds

    def test_delete_nonexistent(self):
        want = [{"community": "unknown"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == []
