"""Unit tests for class_map_match module command builder."""

from class_map_match import _build_commands


def test_match_access_group():
    assert _build_commands("class-home-user", "access-group-name", "acl-home-user", "present") == [
        "class-map class-home-user",
        "match access-group name acl-home-user",
        "exit",
    ]


def test_match_cos():
    assert _build_commands("cos", "cos", "1,2,3", "present") == [
        "class-map cos",
        "match cos 1,2,3",
        "exit",
    ]


def test_match_ip_dscp():
    assert _build_commands("c1", "ip-dscp", "10,12,14", "present") == [
        "class-map c1",
        "match ip dscp 10,12,14",
        "exit",
    ]


def test_match_protocol_absent():
    assert _build_commands("c2", "protocol", "ipv6", "absent") == [
        "class-map c2",
        "no match protocol ipv6",
        "exit",
    ]
