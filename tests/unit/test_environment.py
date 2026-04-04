"""Unit tests for environment module parsers."""

from environment import _parse_temperatures, _parse_fans, _parse_power

SAMPLE_OUTPUT = """
Detail Temperature Status:
Temperature Descr/ID          Current/Threshold Range
------------------------------------------------------
Central Temperature/1         33C/11~79C
Status code: * temperature is out of threshold range

Detail Fan Status:
--------------------------------------------------------------
Right Fan 1 (OK)     Right Fan 2 (OK)

Detail Power Status:
Power Module      Power Status
----------------  -------------
Power 1           In-operation
"""


def test_parse_temperatures():
    temps = _parse_temperatures(SAMPLE_OUTPUT)
    assert len(temps) == 1
    t = temps[0]
    assert t["name"] == "Central Temperature/1"
    assert t["current_celsius"] == 33
    assert t["threshold_min_celsius"] == 11
    assert t["threshold_max_celsius"] == 79
    assert t["out_of_range"] is False


def test_parse_fans():
    fans = _parse_fans(SAMPLE_OUTPUT)
    assert len(fans) == 2
    assert fans[0] == {"name": "Right Fan 1", "status": "OK"}
    assert fans[1] == {"name": "Right Fan 2", "status": "OK"}


def test_parse_power():
    power = _parse_power(SAMPLE_OUTPUT)
    assert len(power) == 1
    assert power[0] == {"module": "Power 1", "status": "In-operation"}


def test_temperature_out_of_range():
    output = """
Detail Temperature Status:
Temperature Descr/ID          Current/Threshold Range
------------------------------------------------------
Central Temperature/1         85C/11~79C *
Status code: * temperature is out of threshold range
"""
    temps = _parse_temperatures(output)
    assert temps[0]["out_of_range"] is True
    assert temps[0]["current_celsius"] == 85
