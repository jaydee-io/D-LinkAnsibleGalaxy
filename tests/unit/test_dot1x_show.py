"""Unit tests for dot1x_show module parsers."""

from dot1x_show import _parse_global, _parse_interface

GLOBAL_OUTPUT = """
802.1X       : Enabled
Trap State   : Enabled
"""

INTERFACE_OUTPUT = """
Interface        : eth1/0/1
PAE              : Authenticator
Control Direction : Both
Port Control     : Auto
Tx Period        : 30 sec
Supp Timeout     : 30 sec
Server Timeout   : 30 sec
Max-req          : 2 times
Forward PDU      : Disabled
"""


def test_parse_global():
    result = _parse_global(GLOBAL_OUTPUT)
    assert result["dot1x_state"] is True
    assert result["trap_state"] is True


def test_parse_global_disabled():
    output = """
802.1X       : Disabled
Trap State   : Disabled
"""
    result = _parse_global(output)
    assert result["dot1x_state"] is False
    assert result["trap_state"] is False


def test_parse_global_empty():
    result = _parse_global("")
    assert result["dot1x_state"] is False
    assert result["trap_state"] is False


def test_parse_interface():
    result = _parse_interface(INTERFACE_OUTPUT)
    assert result["interface"] == "eth1/0/1"
    assert result["pae"] == "Authenticator"
    assert result["control_direction"] == "Both"
    assert result["port_control"] == "Auto"
    assert result["tx_period"] == 30
    assert result["supp_timeout"] == 30
    assert result["server_timeout"] == 30
    assert result["max_req"] == 2
    assert result["forward_pdu"] is False


def test_parse_interface_custom_values():
    output = """
Interface        : eth1/0/5
PAE              : Authenticator
Control Direction : In
Port Control     : Force-unauthorized
Tx Period        : 10 sec
Supp Timeout     : 15 sec
Server Timeout   : 15 sec
Max-req          : 5 times
Forward PDU      : Enabled
"""
    result = _parse_interface(output)
    assert result["interface"] == "eth1/0/5"
    assert result["control_direction"] == "In"
    assert result["port_control"] == "Force-unauthorized"
    assert result["tx_period"] == 10
    assert result["max_req"] == 5
    assert result["forward_pdu"] is True
