"""Unit tests for dai_show_ip_arp_inspection_log module command builder."""

from dai_show_ip_arp_inspection_log import _build_command


def test_build_command():
    cmd = _build_command()
    assert cmd == "show ip arp inspection log"
