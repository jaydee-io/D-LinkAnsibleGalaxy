"""Unit tests for dgs1250_facts module."""

from dgs1250_facts import (
    _build_commands,
    _parse_version,
    _parse_unit,
    _parse_environment,
    _parse_cpu,
)


# ---------------------------------------------------------------------------
# _build_commands
# ---------------------------------------------------------------------------

def test_build_commands_all():
    subsets, cmds = _build_commands(["all"])
    assert subsets == ["version", "unit", "environment", "cpu"]
    assert cmds == [
        "show version",
        "show unit",
        "show environment",
        "show cpu utilization",
    ]


def test_build_commands_single():
    subsets, cmds = _build_commands(["cpu"])
    assert subsets == ["cpu"]
    assert cmds == ["show cpu utilization"]


def test_build_commands_multiple():
    subsets, cmds = _build_commands(["version", "environment"])
    assert subsets == ["version", "environment"]
    assert cmds == ["show version", "show environment"]


def test_build_commands_preserves_order():
    subsets, cmds = _build_commands(["cpu", "version"])
    assert subsets == ["version", "cpu"]
    assert cmds == ["show version", "show cpu utilization"]


# ---------------------------------------------------------------------------
# _parse_version
# ---------------------------------------------------------------------------

SHOW_VERSION_OUTPUT = """\
System MAC Address: F0-7D-68-12-50-01
Module Name DGS-1250-28XMP
H/W A1
Runtime 2.04.P003
"""


def test_parse_version():
    result = _parse_version(SHOW_VERSION_OUTPUT)
    assert result["system_mac_address"] == "F0-7D-68-12-50-01"
    assert result["module_name"] == "DGS-1250-28XMP"
    assert result["hardware_version"] == "A1"
    assert result["runtime"] == "2.04.P003"


def test_parse_version_empty():
    result = _parse_version("")
    assert result["system_mac_address"] == ""
    assert result["runtime"] == ""


# ---------------------------------------------------------------------------
# _parse_unit
# ---------------------------------------------------------------------------

SHOW_UNIT_OUTPUT = """\
       Model Descr                            Model Name
-------------------------------------------  -----------------------------
 24P 10/100/1000M PoE + 4P 10G SFP+           DGS-1250-28XMP

       Serial-Number                Status        Up Time
---------------------------------  ---------  -----------------
 DGS1250102030                      ok         3DT2H38M59S

 Memory     Total       Used        Free
--------  ----------  ----------  ----------
 DRAM      243268 K    125248 K    118020 K
 FLASH      45220 K     24920 K     20300 K
"""


def test_parse_unit_model():
    result = _parse_unit(SHOW_UNIT_OUTPUT)
    assert result["model"]["model_description"] == "24P 10/100/1000M PoE + 4P 10G SFP+"
    assert result["model"]["model_name"] == "DGS-1250-28XMP"


def test_parse_unit_info():
    result = _parse_unit(SHOW_UNIT_OUTPUT)
    assert result["unit"]["serial_number"] == "DGS1250102030"
    assert result["unit"]["status"] == "ok"
    assert result["unit"]["uptime"]["days"] == 3
    assert result["unit"]["uptime"]["hours"] == 2
    assert result["unit"]["uptime"]["minutes"] == 38
    assert result["unit"]["uptime"]["seconds"] == 59
    assert result["unit"]["uptime_raw"] == 3 * 86400 + 2 * 3600 + 38 * 60 + 59


def test_parse_unit_memory():
    result = _parse_unit(SHOW_UNIT_OUTPUT)
    assert len(result["memory"]) == 2
    assert result["memory"][0]["type"] == "DRAM"
    assert result["memory"][0]["total_kb"] == 243268
    assert result["memory"][0]["used_kb"] == 125248
    assert result["memory"][0]["free_kb"] == 118020
    assert result["memory"][1]["type"] == "FLASH"


# ---------------------------------------------------------------------------
# _parse_environment
# ---------------------------------------------------------------------------

SHOW_ENVIRONMENT_OUTPUT = """\
Detail Temperature Status:
Central Temperature/1         33C/11~79C
Central Temperature/2         35C/11~79C

Detail Fan Status:
Right Fan 1 (OK)     Right Fan 2 (OK)

Detail Power Status:
 Power Module        Status
---------  -----------------
Power 1           In-operation
Power 2           Empty
"""


def test_parse_environment_temperatures():
    result = _parse_environment(SHOW_ENVIRONMENT_OUTPUT)
    assert len(result["temperatures"]) == 2
    assert result["temperatures"][0]["name"] == "Central Temperature/1"
    assert result["temperatures"][0]["current_celsius"] == 33
    assert result["temperatures"][0]["threshold_min_celsius"] == 11
    assert result["temperatures"][0]["threshold_max_celsius"] == 79
    assert result["temperatures"][0]["out_of_range"] is False


def test_parse_environment_fans():
    result = _parse_environment(SHOW_ENVIRONMENT_OUTPUT)
    assert len(result["fans"]) == 2
    assert result["fans"][0]["name"] == "Right Fan 1"
    assert result["fans"][0]["status"] == "OK"


def test_parse_environment_power():
    result = _parse_environment(SHOW_ENVIRONMENT_OUTPUT)
    assert len(result["power"]) == 2
    assert result["power"][0]["module"] == "Power 1"
    assert result["power"][0]["status"] == "In-operation"
    assert result["power"][1]["status"] == "Empty"


# ---------------------------------------------------------------------------
# _parse_cpu
# ---------------------------------------------------------------------------

SHOW_CPU_OUTPUT = """\
CPU Utilization
Five seconds -   12 %
One minute -     15 %
Five minutes -   10 %
"""


def test_parse_cpu():
    result = _parse_cpu(SHOW_CPU_OUTPUT)
    assert result["five_seconds_percent"] == 12
    assert result["one_minute_percent"] == 15
    assert result["five_minutes_percent"] == 10


def test_parse_cpu_empty():
    result = _parse_cpu("")
    assert result["five_seconds_percent"] == 0
    assert result["one_minute_percent"] == 0
    assert result["five_minutes_percent"] == 0
