"""Unit tests for dhcp_relay_show_trusted_sources module command builder."""

from dhcp_relay_show_trusted_sources import _build_command


def test_build_command():
    cmd = _build_command()
    assert cmd == "show ip dhcp relay information trusted-sources"
