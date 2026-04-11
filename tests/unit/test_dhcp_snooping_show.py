"""Unit tests for dhcp_snooping_show module command builder."""

from dhcp_snooping_show import _build_command


def test_show():
    cmd = _build_command()
    assert cmd == "show ip dhcp snooping"
