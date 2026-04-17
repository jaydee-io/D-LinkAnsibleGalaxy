"""Unit tests for snmp_server_user module command builder."""

from snmp_server_user import _build_commands


def test_create_v3_auth_priv():
    assert _build_commands("user1", "public", "v3", False, "md5", "authpw", "privpw", None, "present") == [
        "snmp-server user user1 public v3 auth md5 authpw priv privpw",
    ]


def test_create_v2c():
    assert _build_commands("user1", "public", "v2c", False, None, None, None, None, "present") == [
        "snmp-server user user1 public v2c",
    ]


def test_create_v3_encrypted():
    assert _build_commands("user1", "public", "v3", True, "md5", "AABB", None, None, "present") == [
        "snmp-server user user1 public v3 encrypted auth md5 AABB",
    ]


def test_create_with_acl():
    assert _build_commands("user1", "public", "v1", False, None, None, None, "myacl", "present") == [
        "snmp-server user user1 public v1 access myacl",
    ]


def test_remove():
    assert _build_commands("user1", "public", "v3", False, None, None, None, None, "absent") == [
        "no snmp-server user user1 public v3",
    ]
