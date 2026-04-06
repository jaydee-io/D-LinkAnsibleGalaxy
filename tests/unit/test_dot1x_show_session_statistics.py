"""Unit tests for dot1x_show_session_statistics module parser."""

from dot1x_show_session_statistics import _parse_session_statistics

SINGLE_OUTPUT = """
Eth1/0/1 session statistic counters are following:
SessionOctetsRX                        : 0
SessionOctetsTX                        : 0
SessionFramesRX                        : 0
SessionFramesTX                        : 0
SessionId                              :
SessionAuthenticationMethod            : Remote Authentication Server
SessionTime                            : 0
SessionTerminateCause                  : SupplicantLogoff
SessionUserName                        :
"""

MULTI_OUTPUT = """
Eth1/0/1 session statistic counters are following:
SessionOctetsRX                        : 0
SessionOctetsTX                        : 0
SessionFramesRX                        : 0
SessionFramesTX                        : 0
SessionId                              :
SessionAuthenticationMethod            : Remote Authentication Server
SessionTime                            : 0
SessionTerminateCause                  : SupplicantLogoff
SessionUserName                        :

Eth1/0/2 session statistic counters are following:
SessionOctetsRX                        : 1024
SessionOctetsTX                        : 2048
SessionFramesRX                        : 10
SessionFramesTX                        : 20
SessionId                              : 42
SessionAuthenticationMethod            : Remote Authentication Server
SessionTime                            : 300
SessionTerminateCause                  : AuthControlForceUnauth
SessionUserName                        : user1
"""


def test_parse_single_interface():
    results = _parse_session_statistics(SINGLE_OUTPUT)
    assert len(results) == 1
    r = results[0]
    assert r["interface"] == "eth1/0/1"
    assert r["session_octets_rx"] == 0
    assert r["session_octets_tx"] == 0
    assert r["session_frames_rx"] == 0
    assert r["session_frames_tx"] == 0
    assert r["session_id"] == ""
    assert r["session_authentication_method"] == "Remote Authentication Server"
    assert r["session_time"] == 0
    assert r["session_terminate_cause"] == "SupplicantLogoff"
    assert r["session_user_name"] == ""


def test_parse_multi_interface():
    results = _parse_session_statistics(MULTI_OUTPUT)
    assert len(results) == 2

    r1 = results[0]
    assert r1["interface"] == "eth1/0/1"
    assert r1["session_octets_rx"] == 0
    assert r1["session_time"] == 0

    r2 = results[1]
    assert r2["interface"] == "eth1/0/2"
    assert r2["session_octets_rx"] == 1024
    assert r2["session_octets_tx"] == 2048
    assert r2["session_frames_rx"] == 10
    assert r2["session_frames_tx"] == 20
    assert r2["session_id"] == "42"
    assert r2["session_time"] == 300
    assert r2["session_terminate_cause"] == "AuthControlForceUnauth"
    assert r2["session_user_name"] == "user1"


def test_parse_empty():
    results = _parse_session_statistics("")
    assert results == []
