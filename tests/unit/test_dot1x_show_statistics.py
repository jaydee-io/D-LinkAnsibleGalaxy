"""Unit tests for dot1x_show_statistics module parser."""

from dot1x_show_statistics import _parse_statistics

SINGLE_OUTPUT = """
eth1/0/1 dot1x statistics information:
EAPOL Frames RX                : 1
EAPOL Frames TX                : 4
EAPOL-Start Frames RX          : 0
EAPOL-Req/Id Frames TX         : 6
EAPOL-Logoff Frames RX         : 0
EAPOL-Req Frames TX            : 0
EAPOL-Resp/Id Frames RX        : 0
EAPOL-Resp Frames RX           : 0
Invalid EAPOL Frames RX        : 0
EAP-Length Error Frames RX     : 0
Last EAPOL Frame Version       : 0
Last EAPOL Frame Source        : 00-10-28-00-19-78
"""

MULTI_OUTPUT = """
eth1/0/1 dot1x statistics information:
EAPOL Frames RX                : 1
EAPOL Frames TX                : 4
EAPOL-Start Frames RX          : 0
EAPOL-Req/Id Frames TX         : 6
EAPOL-Logoff Frames RX         : 0
EAPOL-Req Frames TX            : 0
EAPOL-Resp/Id Frames RX        : 0
EAPOL-Resp Frames RX           : 0
Invalid EAPOL Frames RX        : 0
EAP-Length Error Frames RX     : 0
Last EAPOL Frame Version       : 0
Last EAPOL Frame Source        : 00-10-28-00-19-78

eth1/0/2 dot1x statistics information:
EAPOL Frames RX                : 10
EAPOL Frames TX                : 20
EAPOL-Start Frames RX          : 3
EAPOL-Req/Id Frames TX         : 15
EAPOL-Logoff Frames RX         : 1
EAPOL-Req Frames TX            : 5
EAPOL-Resp/Id Frames RX        : 3
EAPOL-Resp Frames RX           : 2
Invalid EAPOL Frames RX        : 0
EAP-Length Error Frames RX     : 0
Last EAPOL Frame Version       : 2
Last EAPOL Frame Source        : 00-AA-BB-CC-DD-EE
"""


def test_parse_single_interface():
    results = _parse_statistics(SINGLE_OUTPUT)
    assert len(results) == 1
    r = results[0]
    assert r["interface"] == "eth1/0/1"
    assert r["eapol_frames_rx"] == 1
    assert r["eapol_frames_tx"] == 4
    assert r["eapol_start_frames_rx"] == 0
    assert r["eapol_req_id_frames_tx"] == 6
    assert r["eapol_logoff_frames_rx"] == 0
    assert r["eapol_req_frames_tx"] == 0
    assert r["eapol_resp_id_frames_rx"] == 0
    assert r["eapol_resp_frames_rx"] == 0
    assert r["invalid_eapol_frames_rx"] == 0
    assert r["eap_length_error_frames_rx"] == 0
    assert r["last_eapol_frame_version"] == 0
    assert r["last_eapol_frame_source"] == "00-10-28-00-19-78"


def test_parse_multi_interface():
    results = _parse_statistics(MULTI_OUTPUT)
    assert len(results) == 2

    r1 = results[0]
    assert r1["interface"] == "eth1/0/1"
    assert r1["eapol_frames_rx"] == 1
    assert r1["eapol_frames_tx"] == 4

    r2 = results[1]
    assert r2["interface"] == "eth1/0/2"
    assert r2["eapol_frames_rx"] == 10
    assert r2["eapol_frames_tx"] == 20
    assert r2["eapol_start_frames_rx"] == 3
    assert r2["eapol_logoff_frames_rx"] == 1
    assert r2["eapol_resp_frames_rx"] == 2
    assert r2["last_eapol_frame_version"] == 2
    assert r2["last_eapol_frame_source"] == "00-AA-BB-CC-DD-EE"


def test_parse_empty():
    results = _parse_statistics("")
    assert results == []
