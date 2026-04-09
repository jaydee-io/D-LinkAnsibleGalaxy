"""Unit tests for dhcp_client_lease module command builder."""

from dhcp_client_lease import _build_commands


def test_days_only():
    cmds = _build_commands("vlan 100", 5, None, None, "present")
    assert cmds == ["interface vlan 100", "ip dhcp client lease 5", "exit"]


def test_days_and_hours():
    cmds = _build_commands("vlan 100", 1, 12, None, "present")
    assert cmds == ["interface vlan 100", "ip dhcp client lease 1 12", "exit"]


def test_days_hours_minutes():
    cmds = _build_commands("vlan 100", 1, 12, 30, "present")
    assert cmds == ["interface vlan 100", "ip dhcp client lease 1 12 30", "exit"]


def test_disable():
    cmds = _build_commands("vlan 100", None, None, None, "absent")
    assert cmds == ["interface vlan 100", "no ip dhcp client lease", "exit"]
