"""Unit tests for snmp_server_group module command builder."""

from snmp_server_group import _build_commands


def test_create_v3_auth():
    assert _build_commands("guestgroup", "v3-auth", "interfacesMibView", None, None, None, "present") == [
        "snmp-server group guestgroup v3 auth read interfacesMibView",
    ]


def test_create_v2c_full():
    assert _build_commands("grp", "v2c", "RV", "WV", "NV", None, "present") == [
        "snmp-server group grp v2c read RV write WV notify NV",
    ]


def test_remove():
    assert _build_commands("guestgroup", "v3-auth", None, None, None, None, "absent") == [
        "no snmp-server group guestgroup v3 auth",
    ]
