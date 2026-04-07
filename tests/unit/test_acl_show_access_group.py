"""Unit tests for show_access_group module parser."""

from acl_show_access_group import _parse_access_groups

SAMPLE_OUTPUT = """
eth1/0/1:
  Inbound mac access-list : simple-mac-acl(ID: 7998)
  Inbound ip access-list : simple-ip-acl(ID: 1998)

"""

MULTI_OUTPUT = """
eth1/0/1:
  Inbound mac access-list : simple-mac-acl(ID: 7998)
  Inbound ip access-list : simple-ip-acl(ID: 1998)

eth1/0/3:
  Inbound ipv6 access-list : ip6-control(ID: 14999)

"""


def test_parse_single_interface():
    results = _parse_access_groups(SAMPLE_OUTPUT)
    assert len(results) == 1
    r = results[0]
    assert r["interface"] == "eth1/0/1"
    assert r["mac_acl"] == "simple-mac-acl(ID: 7998)"
    assert r["ip_acl"] == "simple-ip-acl(ID: 1998)"
    assert r["ipv6_acl"] == ""


def test_parse_multi_interface():
    results = _parse_access_groups(MULTI_OUTPUT)
    assert len(results) == 2
    assert results[0]["interface"] == "eth1/0/1"
    assert results[0]["mac_acl"] == "simple-mac-acl(ID: 7998)"
    assert results[1]["interface"] == "eth1/0/3"
    assert results[1]["ipv6_acl"] == "ip6-control(ID: 14999)"
    assert results[1]["mac_acl"] == ""
    assert results[1]["ip_acl"] == ""


def test_parse_empty():
    results = _parse_access_groups("")
    assert results == []
