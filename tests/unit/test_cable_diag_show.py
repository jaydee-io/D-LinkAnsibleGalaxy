"""Unit tests for cable_diag_show module parser."""

from cable_diag_show import _parse_cable_diag


def test_empty():
    result = _parse_cable_diag("")
    assert result == {}


def test_output():
    output = (
        "Port       Type        Link Status  Test Result                     Cable Length (M)\n"
        "---------- ----------- ------------ --------------------------- ------------------\n"
        "eth1/0/1   1000BASE-T Link Up      Pair 1 Open     at    0M    -\n"
    )
    result = _parse_cable_diag(output)
    assert result == {}
