"""Unit tests for dgs1250_l2_interfaces resource module."""

from dgs1250_l2_interfaces import (
    _parse_l2_interfaces,
    _build_commands_merged,
    _build_commands_replaced,
    _build_commands_deleted,
    _index_by_name,
)


RUNNING_CONFIG = """\
interface eth1/0/1
 switchport mode access
 switchport access vlan 100
!
interface eth1/0/2
 switchport mode trunk
 switchport trunk native vlan 10
 switchport trunk allowed vlan add 100,200
!
interface eth1/0/3
!
"""


def _parsed():
    return _parse_l2_interfaces(RUNNING_CONFIG)


def _have_idx():
    return _index_by_name(_parsed())


# ---- parser ----

class TestParser:
    def test_parse_access_port(self):
        idx = _have_idx()
        assert idx["eth1/0/1"]["mode"] == "access"
        assert idx["eth1/0/1"]["access"]["vlan_id"] == 100

    def test_parse_trunk_port(self):
        idx = _have_idx()
        assert idx["eth1/0/2"]["mode"] == "trunk"
        assert idx["eth1/0/2"]["trunk"]["native_vlan"] == 10
        assert sorted(idx["eth1/0/2"]["trunk"]["allowed_vlans"]) == [100, 200]

    def test_parse_default_port(self):
        idx = _have_idx()
        assert idx["eth1/0/3"]["mode"] == "hybrid"
        assert idx["eth1/0/3"]["access"]["vlan_id"] == 1

    def test_parse_trunk_vlan_range(self):
        config = """\
interface eth1/0/5
 switchport mode trunk
 switchport trunk allowed vlan add 100-103
!
"""
        ifaces = _parse_l2_interfaces(config)
        assert sorted(ifaces[0]["trunk"]["allowed_vlans"]) == [100, 101, 102, 103]

    def test_parse_empty_config(self):
        assert _parse_l2_interfaces("") == []


# ---- merged ----

class TestMerged:
    def test_set_access_vlan(self):
        want = [{"name": "eth1/0/3", "mode": "access", "access": {"vlan_id": 200}}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "interface eth1/0/3" in cmds
        assert "switchport mode access" in cmds
        assert "switchport access vlan 200" in cmds

    def test_no_change(self):
        want = [{"name": "eth1/0/1", "mode": "access", "access": {"vlan_id": 100}}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == []

    def test_add_trunk_vlans(self):
        want = [{"name": "eth1/0/2", "trunk": {"allowed_vlans": [100, 200, 300]}}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "interface eth1/0/2" in cmds
        assert "switchport trunk allowed vlan add 300" in cmds

    def test_change_native_vlan(self):
        want = [{"name": "eth1/0/2", "trunk": {"native_vlan": 20}}]
        cmds = _build_commands_merged(want, _have_idx())
        assert "switchport trunk native vlan 20" in cmds

    def test_trunk_vlans_already_present(self):
        want = [{"name": "eth1/0/2", "trunk": {"allowed_vlans": [100, 200]}}]
        cmds = _build_commands_merged(want, _have_idx())
        assert cmds == []


# ---- replaced ----

class TestReplaced:
    def test_replace_access_to_trunk(self):
        want = [{
            "name": "eth1/0/1",
            "mode": "trunk",
            "trunk": {"native_vlan": 1, "allowed_vlans": [100]},
        }]
        cmds = _build_commands_replaced(want, _have_idx())
        assert "interface eth1/0/1" in cmds
        assert "switchport mode trunk" in cmds

    def test_replace_removes_extra_vlans(self):
        want = [{
            "name": "eth1/0/2",
            "mode": "trunk",
            "trunk": {"native_vlan": 10, "allowed_vlans": [100]},
        }]
        cmds = _build_commands_replaced(want, _have_idx())
        assert "switchport trunk allowed vlan remove 200" in cmds

    def test_replace_no_change(self):
        want = [{
            "name": "eth1/0/2",
            "mode": "trunk",
            "trunk": {"native_vlan": 10, "allowed_vlans": [100, 200]},
        }]
        cmds = _build_commands_replaced(want, _have_idx())
        assert cmds == []

    def test_replace_to_default(self):
        want = [{"name": "eth1/0/1"}]
        cmds = _build_commands_replaced(want, _have_idx())
        assert "no switchport mode" not in cmds or "switchport mode hybrid" not in cmds
        assert "no switchport access vlan" in cmds


# ---- deleted ----

class TestDeleted:
    def test_delete_access_port(self):
        want = [{"name": "eth1/0/1"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert "interface eth1/0/1" in cmds
        assert "no switchport mode" in cmds
        assert "no switchport access vlan" in cmds

    def test_delete_trunk_port(self):
        want = [{"name": "eth1/0/2"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert "interface eth1/0/2" in cmds
        assert "no switchport mode" in cmds
        assert "no switchport trunk native vlan" in cmds
        assert "no switchport trunk allowed vlan" in cmds

    def test_delete_default_port_noop(self):
        want = [{"name": "eth1/0/3"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == []

    def test_delete_nonexistent(self):
        want = [{"name": "eth1/0/99"}]
        cmds = _build_commands_deleted(want, _have_idx())
        assert cmds == []

    def test_delete_all(self):
        cmds = _build_commands_deleted([], _have_idx())
        assert "interface eth1/0/1" in cmds
        assert "interface eth1/0/2" in cmds
