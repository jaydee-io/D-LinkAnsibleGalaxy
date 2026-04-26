"""Unit tests for dgs1250_vlans resource module."""

from dgs1250_vlans import (
    _build_commands_merged,
    _build_commands_replaced,
    _build_commands_overridden,
    _build_commands_deleted,
    _index_by_id,
)


HAVE = [
    {"vlan_id": 1, "name": "default"},
    {"vlan_id": 100, "name": "management"},
    {"vlan_id": 200, "name": "servers"},
]


def _have_idx():
    return _index_by_id(HAVE)


# ---- merged ----

class TestMerged:
    def test_create_new_vlan(self):
        want = [{"vlan_id": 300, "name": "guests"}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == ["vlan 300", "name guests", "exit"]

    def test_create_vlan_without_name(self):
        want = [{"vlan_id": 300}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == ["vlan 300", "exit"]

    def test_update_name(self):
        want = [{"vlan_id": 100, "name": "mgmt"}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == ["vlan 100", "name mgmt", "exit"]

    def test_no_change(self):
        want = [{"vlan_id": 100, "name": "management"}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == []

    def test_existing_vlan_no_name_change(self):
        want = [{"vlan_id": 100}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == []

    def test_multiple_vlans(self):
        want = [
            {"vlan_id": 100, "name": "management"},
            {"vlan_id": 300, "name": "guests"},
        ]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == ["vlan 300", "name guests", "exit"]


# ---- replaced ----

class TestReplaced:
    def test_replace_name(self):
        want = [{"vlan_id": 100, "name": "mgmt"}]
        cmds = _build_commands_replaced(want, _have_idx())
        assert cmds == ["vlan 100", "name mgmt", "exit"]

    def test_replace_remove_name(self):
        want = [{"vlan_id": 100}]
        cmds = _build_commands_replaced(want, _have_idx())
        assert cmds == ["vlan 100", "no name", "exit"]

    def test_replace_no_change(self):
        want = [{"vlan_id": 100, "name": "management"}]
        cmds = _build_commands_replaced(want, _have_idx())
        assert cmds == []

    def test_replace_new_vlan(self):
        want = [{"vlan_id": 400, "name": "new"}]
        cmds = _build_commands_replaced(want, _have_idx())
        assert cmds == ["vlan 400", "name new", "exit"]


# ---- overridden ----

class TestOverridden:
    def test_override_removes_extra(self):
        want = [{"vlan_id": 100, "name": "management"}]
        cmds = _build_commands_overridden(want, _have_idx())
        assert "no vlan 200" in cmds
        assert "no vlan 1" not in cmds

    def test_override_no_change(self):
        want = [
            {"vlan_id": 100, "name": "management"},
            {"vlan_id": 200, "name": "servers"},
        ]
        cmds = _build_commands_overridden(want, _have_idx())
        assert cmds == []

    def test_override_add_and_remove(self):
        want = [
            {"vlan_id": 100, "name": "management"},
            {"vlan_id": 300, "name": "guests"},
        ]
        cmds = _build_commands_overridden(want, _have_idx())
        assert "no vlan 200" in cmds
        assert "vlan 300" in cmds
        assert "name guests" in cmds

    def test_override_preserves_vlan1(self):
        want = []
        cmds = _build_commands_overridden(want, _have_idx())
        assert "no vlan 1" not in cmds
        assert "no vlan 100" in cmds
        assert "no vlan 200" in cmds


# ---- deleted ----

class TestDeleted:
    def test_delete_specific(self):
        want = [{"vlan_id": 200}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == ["no vlan 200"]

    def test_delete_all_non_default(self):
        cmds = _build_commands_deleted([], _have_idx())
        assert "no vlan 100" in cmds
        assert "no vlan 200" in cmds
        assert "no vlan 1" not in cmds

    def test_delete_nonexistent(self):
        want = [{"vlan_id": 999}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == []

    def test_delete_vlan1_skipped(self):
        want = [{"vlan_id": 1}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == []


# ---- diff output ----

class TestDiff:
    def test_diff_prepared_format(self):
        commands = _build_commands_merged(
            [{"vlan_id": 300, "name": "guests"}], _have_idx())
        diff = {'prepared': '\n'.join(commands) + '\n'}
        assert diff['prepared'] == "vlan 300\nname guests\nexit\n"

    def test_diff_not_set_when_no_commands(self):
        commands = _build_commands_merged(
            [{"vlan_id": 100, "name": "management"}], _have_idx())
        assert commands == []

    def test_diff_prepared_deleted(self):
        commands = _build_commands_deleted(
            [{"vlan_id": 200}], _have_idx())
        diff = {'prepared': '\n'.join(commands) + '\n'}
        assert diff['prepared'] == "no vlan 200\n"

    def test_diff_prepared_overridden(self):
        commands = _build_commands_overridden(
            [{"vlan_id": 100, "name": "management"}], _have_idx())
        diff = {'prepared': '\n'.join(commands) + '\n'}
        assert "no vlan 200" in diff['prepared']
