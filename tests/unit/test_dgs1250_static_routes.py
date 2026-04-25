"""Unit tests for dgs1250_static_routes resource module."""

from dgs1250_static_routes import (
    _parse_static_routes,
    _build_commands_merged,
    _build_commands_overridden,
    _build_commands_deleted,
    _index_by_key,
)


CONFIG = """\
ip route 10.0.0.0 255.255.255.0 192.168.1.1
ip route 172.16.0.0 255.255.0.0 192.168.1.1 10
"""


def _have():
    return _parse_static_routes(CONFIG)


def _have_idx():
    return _index_by_key(_have())


class TestParser:
    def test_parse_basic(self):
        routes = _have()
        assert len(routes) == 2
        assert routes[0]["prefix"] == "10.0.0.0"
        assert routes[0]["next_hop"] == "192.168.1.1"
        assert "metric" not in routes[0]

    def test_parse_with_metric(self):
        routes = _have()
        assert routes[1]["metric"] == 10

    def test_parse_empty(self):
        assert _parse_static_routes("") == []


class TestMerged:
    def test_add_new(self):
        want = [{"prefix": "192.168.0.0", "mask": "255.255.255.0", "next_hop": "10.0.0.1"}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "ip route 192.168.0.0 255.255.255.0 10.0.0.1" in cmds

    def test_no_change(self):
        want = [{"prefix": "10.0.0.0", "mask": "255.255.255.0", "next_hop": "192.168.1.1"}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == []

    def test_change_metric(self):
        want = [{"prefix": "172.16.0.0", "mask": "255.255.0.0", "next_hop": "192.168.1.1", "metric": 20}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "no ip route 172.16.0.0 255.255.0.0 192.168.1.1" in cmds
        assert "ip route 172.16.0.0 255.255.0.0 192.168.1.1 20" in cmds


class TestOverridden:
    def test_removes_extra(self):
        want = [{"prefix": "10.0.0.0", "mask": "255.255.255.0", "next_hop": "192.168.1.1"}]
        cmds = _build_commands_overridden(want, _have_idx())
        assert "no ip route 172.16.0.0 255.255.0.0 192.168.1.1" in cmds

    def test_no_change(self):
        want = [
            {"prefix": "10.0.0.0", "mask": "255.255.255.0", "next_hop": "192.168.1.1"},
            {"prefix": "172.16.0.0", "mask": "255.255.0.0", "next_hop": "192.168.1.1", "metric": 10},
        ]
        cmds = _build_commands_overridden(want, _have_idx())
        assert cmds == []


class TestDeleted:
    def test_delete_specific(self):
        want = [{"prefix": "10.0.0.0", "mask": "255.255.255.0", "next_hop": "192.168.1.1"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == ["no ip route 10.0.0.0 255.255.255.0 192.168.1.1"]

    def test_delete_all(self):
        cmds = _build_commands_deleted([], _have_idx())
        assert len(cmds) == 2

    def test_delete_nonexistent(self):
        want = [{"prefix": "1.1.1.0", "mask": "255.255.255.0", "next_hop": "2.2.2.2"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == []
