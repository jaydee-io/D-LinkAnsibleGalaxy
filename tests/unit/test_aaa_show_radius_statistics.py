"""Unit tests for aaa_show_radius_statistics module parser."""

from aaa_show_radius_statistics import _parse_radius_stats

SAMPLE_OUTPUT = """
RADIUS Server: 10.0.0.1:1812
  State                  : Up
  Round Trip Time        : 0
  Access Requests        : 10
  Access Accepts         : 8
  Access Rejects         : 1
  Access Challenges      : 0
  Retransmissions        : 1
  Malformed Responses    : 0
  Bad Authenticators     : 0
  Pending Requests       : 0
  Timeouts               : 0
  Unknown Types          : 0
  Packets Dropped        : 0

RADIUS Server: 10.0.0.2:1812
  State                  : Down
  Round Trip Time        : 0
  Access Requests        : 5
  Access Accepts         : 0
  Access Rejects         : 0
  Access Challenges      : 0
  Retransmissions        : 5
  Malformed Responses    : 0
  Bad Authenticators     : 0
  Pending Requests       : 0
  Timeouts               : 5
  Unknown Types          : 0
  Packets Dropped        : 0
"""


def test_parse_two_servers():
    servers = _parse_radius_stats(SAMPLE_OUTPUT)
    assert len(servers) == 2

    s1 = servers[0]
    assert s1["server"] == "10.0.0.1"
    assert s1["auth_port"] == 1812
    assert s1["state"] == "Up"
    assert s1["access_requests"] == 10
    assert s1["access_accepts"] == 8
    assert s1["access_rejects"] == 1
    assert s1["retransmissions"] == 1
    assert s1["timeouts"] == 0

    s2 = servers[1]
    assert s2["server"] == "10.0.0.2"
    assert s2["state"] == "Down"
    assert s2["access_requests"] == 5
    assert s2["retransmissions"] == 5
    assert s2["timeouts"] == 5


def test_parse_empty():
    servers = _parse_radius_stats("")
    assert servers == []
