"""Unit tests for dgs1250_acls resource module."""

from dgs1250_acls import (
    _parse_acls,
    _build_commands_merged,
    _build_commands_overridden,
    _build_commands_deleted,
    _index_by_name,
)


CONFIG = """\
ip access-list extended mgmt-acl
 permit 10.0.0.0 0.0.0.255 any
 deny any any
!
ip access-list extended web-acl
 permit host 192.168.1.1 any
!
"""


def _have():
    return _parse_acls(CONFIG)


def _have_idx():
    return _index_by_name(_have())


class TestParser:
    def test_parse_acl_names(self):
        acls = _have()
        names = [a["name"] for a in acls]
        assert "mgmt-acl" in names
        assert "web-acl" in names

    def test_parse_rules(self):
        idx = _have_idx()
        rules = idx["mgmt-acl"]["rules"]
        assert len(rules) == 2
        assert rules[0]["action"] == "permit"
        assert rules[0]["source"] == "10.0.0.0 0.0.0.255"
        assert rules[1]["action"] == "deny"
        assert rules[1]["source"] == "any"

    def test_parse_host_rule(self):
        idx = _have_idx()
        rules = idx["web-acl"]["rules"]
        assert rules[0]["source"] == "host 192.168.1.1"

    def test_parse_empty(self):
        assert _parse_acls("") == []


class TestMerged:
    def test_add_new_acl(self):
        want = [{"name": "new-acl", "rules": [
            {"action": "permit", "source": "any", "destination": "any"},
        ]}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "ip access-list extended new-acl" in cmds
        assert "permit any" in cmds
        assert "exit" in cmds

    def test_no_change(self):
        want = [{"name": "mgmt-acl", "rules": [
            {"action": "permit", "source": "10.0.0.0 0.0.0.255", "destination": "any"},
            {"action": "deny", "source": "any", "destination": "any"},
        ]}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == []

    def test_update_rules(self):
        want = [{"name": "mgmt-acl", "rules": [
            {"action": "permit", "source": "10.0.0.0 0.0.0.255", "destination": "any"},
        ]}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "no ip access-list extended mgmt-acl" in cmds
        assert "ip access-list extended mgmt-acl" in cmds


class TestOverridden:
    def test_removes_extra(self):
        want = [{"name": "mgmt-acl", "rules": [
            {"action": "permit", "source": "10.0.0.0 0.0.0.255", "destination": "any"},
            {"action": "deny", "source": "any", "destination": "any"},
        ]}]
        cmds = _build_commands_overridden(want, _have_idx())
        assert "no ip access-list extended web-acl" in cmds

    def test_no_change(self):
        want = [
            {"name": "mgmt-acl", "rules": [
                {"action": "permit", "source": "10.0.0.0 0.0.0.255", "destination": "any"},
                {"action": "deny", "source": "any", "destination": "any"},
            ]},
            {"name": "web-acl", "rules": [
                {"action": "permit", "source": "host 192.168.1.1", "destination": "any"},
            ]},
        ]
        cmds = _build_commands_overridden(want, _have_idx())
        assert cmds == []


class TestDeleted:
    def test_delete_specific(self):
        want = [{"name": "web-acl"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == ["no ip access-list extended web-acl"]

    def test_delete_all(self):
        cmds = _build_commands_deleted([], _have_idx())
        assert "no ip access-list extended mgmt-acl" in cmds
        assert "no ip access-list extended web-acl" in cmds

    def test_delete_nonexistent(self):
        want = [{"name": "unknown"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == []
