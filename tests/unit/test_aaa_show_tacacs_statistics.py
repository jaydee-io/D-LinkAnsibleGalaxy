"""Unit tests for aaa_show_tacacs_statistics module parser."""

from aaa_show_tacacs_statistics import _parse_tacacs_stats

SAMPLE_OUTPUT = """
TACACS+ Server: 10.0.0.1/49, State is Up
  Socket Opens           : 5
  Socket Closes          : 3
  Total Packets Sent     : 20
  Total Packets Recv     : 18
  Reference Count        : 1

TACACS+ Server: 10.0.0.2/49, State is Down
  Socket Opens           : 2
  Socket Closes          : 2
  Total Packets Sent     : 10
  Total Packets Recv     : 0
  Reference Count        : 0
"""


def test_parse_two_servers():
    servers = _parse_tacacs_stats(SAMPLE_OUTPUT)
    assert len(servers) == 2

    s1 = servers[0]
    assert s1["server"] == "10.0.0.1"
    assert s1["port"] == 49
    assert s1["state"] == "Up"
    assert s1["socket_opens"] == 5
    assert s1["socket_closes"] == 3
    assert s1["total_packets_sent"] == 20
    assert s1["total_packets_recv"] == 18
    assert s1["reference_count"] == 1

    s2 = servers[1]
    assert s2["server"] == "10.0.0.2"
    assert s2["state"] == "Down"
    assert s2["total_packets_sent"] == 10
    assert s2["total_packets_recv"] == 0


def test_parse_empty():
    servers = _parse_tacacs_stats("")
    assert servers == []
