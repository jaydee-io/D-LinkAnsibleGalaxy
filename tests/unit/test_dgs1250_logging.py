"""Unit tests for dgs1250_logging resource module."""

from dgs1250_logging import (
    _parse_logging_servers,
    _build_commands_merged,
    _build_commands_overridden,
    _build_commands_deleted,
    _index_by_addr,
)


CONFIG = """\
logging server 192.168.1.100 severity warnings
logging server 10.0.0.1 severity informational facility local0
"""


def _have():
    return _parse_logging_servers(CONFIG)


def _have_idx():
    return _index_by_addr(_have())


class TestParser:
    def test_parse_basic(self):
        idx = _have_idx()
        assert idx["192.168.1.100"]["severity"] == "warnings"
        assert idx["192.168.1.100"]["facility"] == ""

    def test_parse_with_facility(self):
        idx = _have_idx()
        assert idx["10.0.0.1"]["severity"] == "informational"
        assert idx["10.0.0.1"]["facility"] == "local0"

    def test_parse_empty(self):
        assert _parse_logging_servers("") == []


class TestMerged:
    def test_add_new(self):
        want = [{"address": "10.0.0.2", "severity": "errors", "facility": ""}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "logging server 10.0.0.2 severity errors" in cmds

    def test_no_change(self):
        want = [{"address": "192.168.1.100", "severity": "warnings", "facility": ""}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == []

    def test_change_severity(self):
        want = [{"address": "192.168.1.100", "severity": "errors", "facility": ""}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "logging server 192.168.1.100 severity errors" in cmds


class TestOverridden:
    def test_removes_extra(self):
        want = [{"address": "192.168.1.100", "severity": "warnings", "facility": ""}]
        cmds = _build_commands_overridden(want, _have_idx())
        assert "no logging server 10.0.0.1" in cmds

    def test_no_change(self):
        want = [
            {"address": "192.168.1.100", "severity": "warnings", "facility": ""},
            {"address": "10.0.0.1", "severity": "informational", "facility": "local0"},
        ]
        cmds = _build_commands_overridden(want, _have_idx())
        assert cmds == []


class TestDeleted:
    def test_delete_specific(self):
        want = [{"address": "10.0.0.1"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == ["no logging server 10.0.0.1"]

    def test_delete_all(self):
        cmds = _build_commands_deleted([], _have_idx())
        assert len(cmds) == 2

    def test_delete_nonexistent(self):
        want = [{"address": "1.2.3.4"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == []
