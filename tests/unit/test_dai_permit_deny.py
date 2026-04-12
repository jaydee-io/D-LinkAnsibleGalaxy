"""Unit tests for dai_permit_deny module command builder."""

from dai_permit_deny import _build_commands


def test_permit_ip_subnet_mac_any():
    cmds = _build_commands("static-arp-list", "permit", False, None, "10.20.0.0", "255.255.0.0",
                           True, None, None, None, "present")
    assert cmds == [
        "arp access-list static-arp-list",
        "permit ip 10.20.0.0 255.255.0.0 mac any",
        "exit",
    ]


def test_permit_ip_any_mac_host():
    cmds = _build_commands("mylist", "permit", True, None, None, None,
                           False, "00:11:22:33:44:55", None, None, "present")
    assert cmds == [
        "arp access-list mylist",
        "permit ip any mac host 00:11:22:33:44:55",
        "exit",
    ]


def test_deny_ip_host_mac_any():
    cmds = _build_commands("mylist", "deny", False, "192.168.1.1", None, None,
                           True, None, None, None, "present")
    assert cmds == [
        "arp access-list mylist",
        "deny ip host 192.168.1.1 mac any",
        "exit",
    ]


def test_remove():
    cmds = _build_commands("static-arp-list", "permit", False, None, "10.20.0.0", "255.255.0.0",
                           True, None, None, None, "absent")
    assert cmds == [
        "arp access-list static-arp-list",
        "no permit ip 10.20.0.0 255.255.0.0 mac any",
        "exit",
    ]
