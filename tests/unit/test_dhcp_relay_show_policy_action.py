"""Unit tests for dhcp_relay_show_policy_action module command builder."""

from dhcp_relay_show_policy_action import _build_command


def test_build_command():
    cmd = _build_command()
    assert cmd == "show ip dhcp relay information policy-action"
