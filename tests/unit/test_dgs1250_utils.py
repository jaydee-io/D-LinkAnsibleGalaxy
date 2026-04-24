"""Unit tests for module_utils/dgs1250.py mode detection and transitions."""

from unittest.mock import MagicMock

from dgs1250 import (
    _detect_mode,
    _config_commands,
    _expand_command,
    _expand_interface_spec,
    _parse_numeric_list,
    ensure_mode,
    MODE_USER,
    MODE_PRIVILEGED,
    MODE_GLOBAL_CONFIG,
)


def _mock_connection(prompt_bytes):
    """Return a mock Connection whose get_prompt returns prompt_bytes."""
    conn = MagicMock()
    conn.get_prompt.return_value = prompt_bytes
    return conn


# ---- _detect_mode ----------------------------------------------------------

def test_detect_user_mode():
    assert _detect_mode(_mock_connection(b"Switch>")) == MODE_USER


def test_detect_user_mode_with_space():
    assert _detect_mode(_mock_connection(b"Switch> ")) == MODE_USER


def test_detect_privileged_mode():
    assert _detect_mode(_mock_connection(b"Switch#")) == MODE_PRIVILEGED


def test_detect_privileged_mode_with_space():
    assert _detect_mode(_mock_connection(b"Switch# ")) == MODE_PRIVILEGED


def test_detect_global_config_mode():
    assert _detect_mode(_mock_connection(b"Switch(config)#")) == MODE_GLOBAL_CONFIG


def test_detect_config_if_mode():
    assert _detect_mode(_mock_connection(b"Switch(config-if)#")) == MODE_GLOBAL_CONFIG


def test_detect_config_line_mode():
    assert _detect_mode(_mock_connection(b"Switch(config-line)#")) == MODE_GLOBAL_CONFIG


def test_detect_config_vlan_mode():
    assert _detect_mode(_mock_connection(b"Switch(config-vlan)#")) == MODE_GLOBAL_CONFIG


def test_detect_config_with_trailing_space():
    assert _detect_mode(_mock_connection(b"Switch(config)# ")) == MODE_GLOBAL_CONFIG


def test_detect_custom_hostname():
    assert _detect_mode(_mock_connection(b"MySwitch-01#")) == MODE_PRIVILEGED


def test_detect_custom_hostname_user():
    assert _detect_mode(_mock_connection(b"MySwitch-01>")) == MODE_USER


# ---- ensure_mode: no-op when already in target mode ------------------------

def test_ensure_mode_noop_user():
    conn = _mock_connection(b"Switch>")
    ensure_mode(conn, MODE_USER)
    conn.get.assert_not_called()


def test_ensure_mode_noop_privileged():
    conn = _mock_connection(b"Switch#")
    ensure_mode(conn, MODE_PRIVILEGED)
    conn.get.assert_not_called()


def test_ensure_mode_noop_global_config():
    conn = _mock_connection(b"Switch(config)#")
    ensure_mode(conn, MODE_GLOBAL_CONFIG)
    conn.get.assert_not_called()


# ---- ensure_mode: escalation -----------------------------------------------

def test_escalate_user_to_privileged():
    conn = _mock_connection(b"Switch>")
    ensure_mode(conn, MODE_PRIVILEGED)
    conn.get.assert_called_once_with("enable")


def test_escalate_user_to_global_config():
    conn = _mock_connection(b"Switch>")
    ensure_mode(conn, MODE_GLOBAL_CONFIG)
    assert conn.get.call_count == 2
    conn.get.assert_any_call("enable")
    conn.get.assert_any_call("configure terminal")


def test_escalate_privileged_to_global_config():
    conn = _mock_connection(b"Switch#")
    ensure_mode(conn, MODE_GLOBAL_CONFIG)
    conn.get.assert_called_once_with("configure terminal")


# ---- ensure_mode: de-escalation --------------------------------------------

def test_deescalate_global_config_to_privileged():
    conn = _mock_connection(b"Switch(config)#")
    ensure_mode(conn, MODE_PRIVILEGED)
    conn.get.assert_called_once_with("end")


def test_deescalate_global_config_to_user():
    conn = _mock_connection(b"Switch(config)#")
    ensure_mode(conn, MODE_USER)
    assert conn.get.call_count == 2
    conn.get.assert_any_call("end")
    conn.get.assert_any_call("disable")


def test_deescalate_privileged_to_user():
    conn = _mock_connection(b"Switch#")
    ensure_mode(conn, MODE_USER)
    conn.get.assert_called_once_with("disable")


def test_deescalate_config_if_to_privileged():
    conn = _mock_connection(b"Switch(config-if)#")
    ensure_mode(conn, MODE_PRIVILEGED)
    conn.get.assert_called_once_with("end")


# ---- _config_commands -------------------------------------------------------

def test_config_commands_simple():
    assert _config_commands(["sntp enable"]) == ["sntp enable"]


def test_config_commands_no_prefix():
    assert _config_commands(["no sntp enable"]) == ["no sntp enable"]


def test_config_commands_interface_scoped():
    cmds = ["interface ethernet 1/0/1", "spanning-tree portfast", "exit"]
    assert _config_commands(cmds) == ["spanning-tree portfast"]


def test_config_commands_subconfig():
    cmds = ["aaa server radius dynamic-author", "client 10.0.0.1 server-key secret", "exit"]
    assert _config_commands(cmds) == ["client 10.0.0.1 server-key secret"]


def test_config_commands_interface_range():
    cmds = ["interface range ethernet 1/0/1-8", "storm-control broadcast level 80", "exit"]
    assert _config_commands(cmds) == ["storm-control broadcast level 80"]


def test_config_commands_ip_dhcp_pool():
    cmds = ["ip dhcp pool MYPOOL", "network 192.168.1.0 255.255.255.0", "exit"]
    assert _config_commands(cmds) == ["network 192.168.1.0 255.255.255.0"]


def test_config_commands_class_map():
    cmds = ["class-map match-all MYCLASS", "match access-group name MYACL", "exit"]
    assert _config_commands(cmds) == ["match access-group name MYACL"]


def test_config_commands_policy_map():
    cmds = ["policy-map MYPOLICY", "class MYCLASS", "exit"]
    assert _config_commands(cmds) == ["class MYCLASS"]


def test_config_commands_ip_access_list():
    cmds = ["ip access-list extended MYACL", "permit ip any any", "exit"]
    assert _config_commands(cmds) == ["permit ip any any"]


def test_config_commands_vlan():
    cmds = ["vlan 100", "name SERVERS", "exit"]
    assert _config_commands(cmds) == ["name SERVERS"]


def test_config_commands_line():
    cmds = ["line console 0", "speed 115200", "exit"]
    assert _config_commands(cmds) == ["speed 115200"]


def test_config_commands_empty_payload():
    cmds = ["interface ethernet 1/0/1", "exit"]
    assert _config_commands(cmds) == []


def test_config_commands_multiple_payload():
    cmds = ["interface ethernet 1/0/1", "no shutdown", "description uplink", "exit"]
    assert _config_commands(cmds) == ["no shutdown", "description uplink"]


# ---- _parse_numeric_list ----------------------------------------------------

def test_parse_numeric_list_single():
    assert _parse_numeric_list("10") is None


def test_parse_numeric_list_range():
    assert _parse_numeric_list("1-5") == [1, 2, 3, 4, 5]


def test_parse_numeric_list_csv():
    assert _parse_numeric_list("10,20,30") == [10, 20, 30]


def test_parse_numeric_list_mixed():
    assert _parse_numeric_list("10,15-18") == [10, 15, 16, 17, 18]


def test_parse_numeric_list_multi_range():
    assert _parse_numeric_list("1-3,7-9") == [1, 2, 3, 7, 8, 9]


def test_parse_numeric_list_reversed_range():
    assert _parse_numeric_list("5-1") is None


def test_parse_numeric_list_not_numeric():
    assert _parse_numeric_list("abc") is None


# ---- _expand_interface_spec -------------------------------------------------

def test_expand_iface_single():
    assert _expand_interface_spec("eth1/0/1") is None


def test_expand_iface_range():
    assert _expand_interface_spec("eth1/0/1-4") == [
        "eth1/0/1", "eth1/0/2", "eth1/0/3", "eth1/0/4"]


def test_expand_iface_list():
    assert _expand_interface_spec("eth1/0/1,eth1/0/5") == [
        "eth1/0/1", "eth1/0/5"]


def test_expand_iface_list_with_range():
    assert _expand_interface_spec("eth1/0/1-3,eth1/0/7") == [
        "eth1/0/1", "eth1/0/2", "eth1/0/3", "eth1/0/7"]


def test_expand_iface_high_ports():
    assert _expand_interface_spec("eth1/0/10-12") == [
        "eth1/0/10", "eth1/0/11", "eth1/0/12"]


# ---- _expand_command --------------------------------------------------------

def test_expand_cmd_no_range():
    assert _expand_command("sntp enable") == ["sntp enable"]


def test_expand_cmd_single_interface():
    assert _expand_command("mac-address-table learning interface eth1/0/5") == [
        "mac-address-table learning interface eth1/0/5"]


def test_expand_cmd_interface_range():
    assert _expand_command("mac-address-table learning interface eth1/0/1-3") == [
        "mac-address-table learning interface eth1/0/1",
        "mac-address-table learning interface eth1/0/2",
        "mac-address-table learning interface eth1/0/3",
    ]


def test_expand_cmd_no_interface_range():
    assert _expand_command("no mac-address-table learning interface eth1/0/1-3") == [
        "no mac-address-table learning interface eth1/0/1",
        "no mac-address-table learning interface eth1/0/2",
        "no mac-address-table learning interface eth1/0/3",
    ]


def test_expand_cmd_interface_list():
    assert _expand_command("mac-address-table learning interface eth1/0/1,eth1/0/5") == [
        "mac-address-table learning interface eth1/0/1",
        "mac-address-table learning interface eth1/0/5",
    ]


def test_expand_cmd_interface_with_suffix():
    assert _expand_command("monitor session 1 source interface eth1/0/2-4 rx") == [
        "monitor session 1 source interface eth1/0/2 rx",
        "monitor session 1 source interface eth1/0/3 rx",
        "monitor session 1 source interface eth1/0/4 rx",
    ]


def test_expand_cmd_vlan_range():
    assert _expand_command("ip arp inspection vlan 1-3") == [
        "ip arp inspection vlan 1",
        "ip arp inspection vlan 2",
        "ip arp inspection vlan 3",
    ]


def test_expand_cmd_no_vlan_range():
    assert _expand_command("no ip dhcp snooping vlan 10,15-16") == [
        "no ip dhcp snooping vlan 10",
        "no ip dhcp snooping vlan 15",
        "no ip dhcp snooping vlan 16",
    ]


def test_expand_cmd_vlan_with_suffix():
    assert _expand_command("ip arp inspection vlan 1-2 logging deny") == [
        "ip arp inspection vlan 1 logging deny",
        "ip arp inspection vlan 2 logging deny",
    ]


def test_expand_cmd_switchport_trunk():
    assert _expand_command("switchport trunk allowed vlan add 100-102") == [
        "switchport trunk allowed vlan add 100",
        "switchport trunk allowed vlan add 101",
        "switchport trunk allowed vlan add 102",
    ]


def test_expand_cmd_switchport_hybrid_mixed():
    assert _expand_command("switchport hybrid allowed vlan add tagged 10,20-22") == [
        "switchport hybrid allowed vlan add tagged 10",
        "switchport hybrid allowed vlan add tagged 20",
        "switchport hybrid allowed vlan add tagged 21",
        "switchport hybrid allowed vlan add tagged 22",
    ]


def test_expand_cmd_single_vlan():
    assert _expand_command("ip arp inspection vlan 10") == [
        "ip arp inspection vlan 10"]


def test_expand_cmd_time_range_not_expanded():
    """time-range contains a dash but is not a numeric range."""
    assert _expand_command("power-saving hibernation time-range myprofile") == [
        "power-saving hibernation time-range myprofile"]
