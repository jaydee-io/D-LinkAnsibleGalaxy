"""Unit tests for show_ip_source_binding module."""

from show_ip_source_binding import _build_command


def test_no_params():
    assert _build_command(None, None, None, None, None) == "show ip source binding"


def test_ip():
    assert _build_command("10.1.1.10", None, None, None, None) == "show ip source binding 10.1.1.10"


def test_static():
    assert _build_command(None, None, "static", None, None) == "show ip source binding static"


def test_all_params():
    assert _build_command("10.1.1.10", "00-01-01-01-01-10", "dhcp-snooping", 100, "eth1/0/3") == (
        "show ip source binding 10.1.1.10 00-01-01-01-01-10 dhcp-snooping vlan 100 interface eth1/0/3"
    )
