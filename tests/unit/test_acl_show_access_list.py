"""Unit tests for show_access_list module parsers."""

from acl_show_access_list import _parse_summary, _parse_detailed

SUMMARY_OUTPUT = """
Access-List-Name                                           Type
-------------------------------------------              ---------------
Strict-Control(ID: 3999)                                 ip ext-acl
daily-profile(ID: 7999)                                  mac ext-acl
ip6-control(ID: 14999)                                   ipv6 ext-acl

Total Entries: 3
"""

DETAILED_OUTPUT = """
Extended IP access list Strict-Control(ID: 3999)
    10 permit any 10.20.0.0 0.0.255.255
    20 permit any host 10.100.1.2
"""

DETAILED_WITH_COUNTER = """
Extended IP access simple-ip-acl(ID:3994)
    10 permit tcp any 10.20.0.0 0.0.255.255 (Ing: 6410 packets Egr: 5201 packets)
    20 permit tcp any host 10.100.1.2   (Ing: 3232 packets Egr: 0 packets)
    30 permit icmp any any   (Ing: 8758 packets Egr: 4214 packets)

    Counter enable on following port(s):
 Ingress port(s): eth1/0/5-1/0/8
"""


def test_parse_summary():
    results = _parse_summary(SUMMARY_OUTPUT)
    assert len(results) == 3
    assert results[0]["name"] == "Strict-Control(ID: 3999)"
    assert results[0]["type"] == "ip ext-acl"
    assert results[1]["name"] == "daily-profile(ID: 7999)"
    assert results[1]["type"] == "mac ext-acl"
    assert results[2]["name"] == "ip6-control(ID: 14999)"
    assert results[2]["type"] == "ipv6 ext-acl"


def test_parse_summary_empty():
    results = _parse_summary("")
    assert results == []


def test_parse_detailed():
    results = _parse_detailed(DETAILED_OUTPUT)
    assert len(results) == 1
    r = results[0]
    assert r["name"] == "Strict-Control(ID: 3999)"
    assert r["type"] == "ip ext-acl"
    assert len(r["rules"]) == 2
    assert r["rules"][0] == "10 permit any 10.20.0.0 0.0.255.255"
    assert r["rules"][1] == "20 permit any host 10.100.1.2"


def test_parse_detailed_with_counter():
    results = _parse_detailed(DETAILED_WITH_COUNTER)
    assert len(results) == 1
    assert len(results[0]["rules"]) == 3
    assert "10 permit tcp any 10.20.0.0 0.0.255.255 (Ing: 6410 packets Egr: 5201 packets)" in results[0]["rules"][0]


def test_parse_detailed_empty():
    results = _parse_detailed("")
    assert results == []
