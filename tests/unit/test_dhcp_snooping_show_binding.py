"""Unit tests for dhcp_snooping_show_binding module command builder."""

from dhcp_snooping_show_binding import _build_command


def test_show_all():
    cmd = _build_command()
    assert cmd == "show ip dhcp snooping binding"


def test_show_by_vlan():
    cmd = _build_command(vlan="100")
    assert cmd == "show ip dhcp snooping binding vlan 100"


def test_show_by_ip():
    cmd = _build_command(ip_address="10.0.0.1")
    assert cmd == "show ip dhcp snooping binding 10.0.0.1"


def test_show_by_mac_and_interface():
    cmd = _build_command(mac_address="00:11:22:33:44:55", interface="ethernet 1/0/1")
    assert cmd == "show ip dhcp snooping binding 00:11:22:33:44:55 interface ethernet 1/0/1"
