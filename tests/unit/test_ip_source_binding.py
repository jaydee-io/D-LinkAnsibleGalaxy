"""Unit tests for ip_source_binding module."""

from ip_source_binding import _build_commands


def test_present():
    assert _build_commands("00-01-02-03-04-05", 2, "10.1.1.1", "eth1/0/10", "present") == [
        "ip source binding 00-01-02-03-04-05 vlan 2 10.1.1.1 interface eth1/0/10"
    ]


def test_absent():
    assert _build_commands("00-01-02-03-04-05", 2, "10.1.1.1", "eth1/0/10", "absent") == [
        "no ip source binding 00-01-02-03-04-05 vlan 2 10.1.1.1 interface eth1/0/10"
    ]
