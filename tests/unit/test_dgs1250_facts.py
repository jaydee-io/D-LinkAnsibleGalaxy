"""Unit tests for dgs1250_facts module."""

from dgs1250_facts import _build_commands
from dgs1250_parsers import (
    parse_version,
    parse_unit,
    parse_environment,
    parse_cpu,
    parse_interfaces,
    parse_vlans,
    parse_mac_table,
    parse_snmp,
    parse_lldp_neighbors,
    parse_stp,
    parse_static_routes,
)


# ---------------------------------------------------------------------------
# _build_commands
# ---------------------------------------------------------------------------

def test_build_commands_all():
    subsets, cmds = _build_commands(["all"])
    assert subsets == ["version", "unit", "environment", "cpu",
                       "interfaces", "vlans", "mac_table",
                       "snmp", "lldp_neighbors", "stp", "static_routes"]
    assert cmds == [
        "show version",
        "show unit",
        "show environment",
        "show cpu utilization",
        "show interfaces status",
        "show vlan",
        "show mac-address-table",
        "show snmp community",
        "show lldp neighbors",
        "show spanning-tree",
        "show ip route static",
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


def test_build_commands_new_subsets():
    subsets, cmds = _build_commands(["interfaces", "vlans", "mac_table"])
    assert subsets == ["interfaces", "vlans", "mac_table"]
    assert cmds == [
        "show interfaces status",
        "show vlan",
        "show mac-address-table",
    ]


def test_build_commands_v2_subsets():
    subsets, cmds = _build_commands(["snmp", "lldp_neighbors", "stp", "static_routes"])
    assert subsets == ["snmp", "lldp_neighbors", "stp", "static_routes"]
    assert cmds == [
        "show snmp community",
        "show lldp neighbors",
        "show spanning-tree",
        "show ip route static",
    ]


# ---------------------------------------------------------------------------
# parse_version
# ---------------------------------------------------------------------------

SHOW_VERSION_OUTPUT = """\
System MAC Address: F0-7D-68-12-50-01
Module Name DGS-1250-28XMP
H/W A1
Runtime 2.04.P003
"""


def test_parse_version():
    result = parse_version(SHOW_VERSION_OUTPUT)
    assert result["system_mac_address"] == "F0-7D-68-12-50-01"
    assert result["module_name"] == "DGS-1250-28XMP"
    assert result["hardware_version"] == "A1"
    assert result["runtime"] == "2.04.P003"


def test_parse_version_empty():
    result = parse_version("")
    assert result["system_mac_address"] == ""
    assert result["runtime"] == ""


# ---------------------------------------------------------------------------
# parse_unit
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
    result = parse_unit(SHOW_UNIT_OUTPUT)
    assert result["model"]["model_description"] == "24P 10/100/1000M PoE + 4P 10G SFP+"
    assert result["model"]["model_name"] == "DGS-1250-28XMP"


def test_parse_unit_info():
    result = parse_unit(SHOW_UNIT_OUTPUT)
    assert result["unit"]["serial_number"] == "DGS1250102030"
    assert result["unit"]["status"] == "ok"
    assert result["unit"]["uptime"]["days"] == 3
    assert result["unit"]["uptime"]["hours"] == 2
    assert result["unit"]["uptime"]["minutes"] == 38
    assert result["unit"]["uptime"]["seconds"] == 59
    assert result["unit"]["uptime_raw"] == 3 * 86400 + 2 * 3600 + 38 * 60 + 59


def test_parse_unit_memory():
    result = parse_unit(SHOW_UNIT_OUTPUT)
    assert len(result["memory"]) == 2
    assert result["memory"][0]["type"] == "DRAM"
    assert result["memory"][0]["total_kb"] == 243268
    assert result["memory"][0]["used_kb"] == 125248
    assert result["memory"][0]["free_kb"] == 118020
    assert result["memory"][1]["type"] == "FLASH"


# ---------------------------------------------------------------------------
# parse_environment
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
    result = parse_environment(SHOW_ENVIRONMENT_OUTPUT)
    assert len(result["temperatures"]) == 2
    assert result["temperatures"][0]["name"] == "Central Temperature/1"
    assert result["temperatures"][0]["current_celsius"] == 33
    assert result["temperatures"][0]["threshold_min_celsius"] == 11
    assert result["temperatures"][0]["threshold_max_celsius"] == 79
    assert result["temperatures"][0]["out_of_range"] is False


def test_parse_environment_fans():
    result = parse_environment(SHOW_ENVIRONMENT_OUTPUT)
    assert len(result["fans"]) == 2
    assert result["fans"][0]["name"] == "Right Fan 1"
    assert result["fans"][0]["status"] == "OK"


def test_parse_environment_power():
    result = parse_environment(SHOW_ENVIRONMENT_OUTPUT)
    assert len(result["power"]) == 2
    assert result["power"][0]["module"] == "Power 1"
    assert result["power"][0]["status"] == "In-operation"
    assert result["power"][1]["status"] == "Empty"


# ---------------------------------------------------------------------------
# parse_cpu
# ---------------------------------------------------------------------------

SHOW_CPU_OUTPUT = """\
CPU Utilization
Five seconds -   12 %
One minute -     15 %
Five minutes -   10 %
"""


def test_parse_cpu():
    result = parse_cpu(SHOW_CPU_OUTPUT)
    assert result["five_seconds_percent"] == 12
    assert result["one_minute_percent"] == 15
    assert result["five_minutes_percent"] == 10


def test_parse_cpu_empty():
    result = parse_cpu("")
    assert result["five_seconds_percent"] == 0
    assert result["one_minute_percent"] == 0
    assert result["five_minutes_percent"] == 0


# ---------------------------------------------------------------------------
# parse_interfaces
# ---------------------------------------------------------------------------

SHOW_INTERFACES_STATUS_OUTPUT = """\
Port          Status        VLAN    Duplex Speed          Type
------------- ------------- ------- ------- ------------- -------------
eth1/0/1      not-connected 1       auto    auto          1000BASE-T
eth1/0/2      connected     1       full    1000M         1000BASE-T
eth1/0/3      disabled      100     auto    auto          1000BASE-T
eth1/0/25     connected     1       full    10G           10GBASE-SR
"""


def test_parse_interfaces():
    result = parse_interfaces(SHOW_INTERFACES_STATUS_OUTPUT)
    assert len(result) == 4
    assert result[0]["port"] == "eth1/0/1"
    assert result[0]["status"] == "not-connected"
    assert result[0]["vlan"] == "1"
    assert result[0]["duplex"] == "auto"
    assert result[0]["speed"] == "auto"
    assert result[0]["type"] == "1000BASE-T"


def test_parse_interfaces_connected():
    result = parse_interfaces(SHOW_INTERFACES_STATUS_OUTPUT)
    assert result[1]["port"] == "eth1/0/2"
    assert result[1]["status"] == "connected"
    assert result[1]["duplex"] == "full"
    assert result[1]["speed"] == "1000M"


def test_parse_interfaces_disabled():
    result = parse_interfaces(SHOW_INTERFACES_STATUS_OUTPUT)
    assert result[2]["port"] == "eth1/0/3"
    assert result[2]["status"] == "disabled"
    assert result[2]["vlan"] == "100"


def test_parse_interfaces_sfp():
    result = parse_interfaces(SHOW_INTERFACES_STATUS_OUTPUT)
    assert result[3]["port"] == "eth1/0/25"
    assert result[3]["speed"] == "10G"
    assert result[3]["type"] == "10GBASE-SR"


def test_parse_interfaces_empty():
    result = parse_interfaces("")
    assert result == []


# ---------------------------------------------------------------------------
# parse_vlans
# ---------------------------------------------------------------------------

SHOW_VLAN_OUTPUT = """\
VLAN 1
Name : default
Description :
Tagged Member Ports :
Untagged Member Ports : eth1/0/1-1/0/28
VLAN 100
Name : Management
Description :
Tagged Member Ports : eth1/0/25-1/0/28
Untagged Member Ports : eth1/0/1-1/0/4
Total Entries : 2
"""


def test_parse_vlans():
    result = parse_vlans(SHOW_VLAN_OUTPUT)
    assert len(result) == 2
    assert result[0]["vlan_id"] == 1
    assert result[0]["name"] == "default"
    assert result[0]["tagged_ports"] == ""
    assert result[0]["untagged_ports"] == "eth1/0/1-1/0/28"


def test_parse_vlans_second():
    result = parse_vlans(SHOW_VLAN_OUTPUT)
    assert result[1]["vlan_id"] == 100
    assert result[1]["name"] == "Management"
    assert result[1]["tagged_ports"] == "eth1/0/25-1/0/28"
    assert result[1]["untagged_ports"] == "eth1/0/1-1/0/4"


def test_parse_vlans_single():
    output = """\
VLAN 42
Name : TestVLAN
Description :
Tagged Member Ports :
Untagged Member Ports :
Total Entries : 1
"""
    result = parse_vlans(output)
    assert len(result) == 1
    assert result[0]["vlan_id"] == 42
    assert result[0]["name"] == "TestVLAN"
    assert result[0]["tagged_ports"] == ""
    assert result[0]["untagged_ports"] == ""


def test_parse_vlans_empty():
    result = parse_vlans("")
    assert result == []


# ---------------------------------------------------------------------------
# parse_mac_table
# ---------------------------------------------------------------------------

SHOW_MAC_TABLE_OUTPUT = """\
VLAN   MAC Address        Type     Ports
------ ------------------ -------- --------
1      00-02-4B-28-C4-82  Static   CPU
1      00-03-40-11-22-33  Dynamic  eth1/0/2
2      C2-F3-22-0A-12-F4  Static   port-channel2
Total Entries: 3
"""


def test_parse_mac_table():
    result = parse_mac_table(SHOW_MAC_TABLE_OUTPUT)
    assert len(result) == 3
    assert result[0]["vlan"] == 1
    assert result[0]["mac_address"] == "00-02-4B-28-C4-82"
    assert result[0]["type"] == "Static"
    assert result[0]["port"] == "CPU"


def test_parse_mac_table_dynamic():
    result = parse_mac_table(SHOW_MAC_TABLE_OUTPUT)
    assert result[1]["vlan"] == 1
    assert result[1]["mac_address"] == "00-03-40-11-22-33"
    assert result[1]["type"] == "Dynamic"
    assert result[1]["port"] == "eth1/0/2"


def test_parse_mac_table_port_channel():
    result = parse_mac_table(SHOW_MAC_TABLE_OUTPUT)
    assert result[2]["vlan"] == 2
    assert result[2]["port"] == "port-channel2"


def test_parse_mac_table_empty():
    result = parse_mac_table("")
    assert result == []


def test_parse_mac_table_colon_format():
    output = """\
VLAN   MAC Address        Type     Ports
------ ------------------ -------- --------
1      00:02:4B:28:C4:82  Dynamic  eth1/0/1
Total Entries: 1
"""
    result = parse_mac_table(output)
    assert len(result) == 1
    assert result[0]["mac_address"] == "00:02:4B:28:C4:82"


# ---------------------------------------------------------------------------
# parse_snmp
# ---------------------------------------------------------------------------

SHOW_SNMP_COMMUNITY_OUTPUT = """\
SNMP Community Table:
Community Name       View Name        Access Right
-------------------  ---------------  ------------
public               CommunityView    Read-Only
private              CommunityView    Read-Write

Total Entries: 2
"""


def test_parse_snmp():
    result = parse_snmp(SHOW_SNMP_COMMUNITY_OUTPUT)
    assert len(result) == 2
    assert result[0]["community"] == "public"
    assert result[0]["view"] == "CommunityView"
    assert result[0]["access"] == "Read-Only"


def test_parse_snmp_rw():
    result = parse_snmp(SHOW_SNMP_COMMUNITY_OUTPUT)
    assert result[1]["community"] == "private"
    assert result[1]["access"] == "Read-Write"


def test_parse_snmp_single():
    output = """\
SNMP Community Table:
Community Name       View Name        Access Right
-------------------  ---------------  ------------
monitor              DefaultView      Read-Only

Total Entries: 1
"""
    result = parse_snmp(output)
    assert len(result) == 1
    assert result[0]["community"] == "monitor"
    assert result[0]["view"] == "DefaultView"


def test_parse_snmp_empty():
    result = parse_snmp("")
    assert result == []


# ---------------------------------------------------------------------------
# parse_lldp_neighbors
# ---------------------------------------------------------------------------

SHOW_LLDP_NEIGHBORS_OUTPUT = """\
System Name    : DGS-1250-28XMP
System Capabilities Supported : Bridge, Router

Local Port  Chassis ID             Port ID            System Name     Hold Time
----------  ---------------------  -----------------  ------------    ---------
eth1/0/1    F0-7D-68-AA-BB-CC      eth1/0/24          Switch-A        120
eth1/0/24   00-11-22-33-44-55      eth1/0/1           Switch-B         90

Total Entries: 2
"""


def test_parse_lldp_neighbors():
    result = parse_lldp_neighbors(SHOW_LLDP_NEIGHBORS_OUTPUT)
    assert len(result) == 2
    assert result[0]["local_port"] == "eth1/0/1"
    assert result[0]["chassis_id"] == "F0-7D-68-AA-BB-CC"
    assert result[0]["port_id"] == "eth1/0/24"
    assert result[0]["system_name"] == "Switch-A"
    assert result[0]["hold_time"] == 120


def test_parse_lldp_neighbors_second():
    result = parse_lldp_neighbors(SHOW_LLDP_NEIGHBORS_OUTPUT)
    assert result[1]["local_port"] == "eth1/0/24"
    assert result[1]["chassis_id"] == "00-11-22-33-44-55"
    assert result[1]["system_name"] == "Switch-B"
    assert result[1]["hold_time"] == 90


def test_parse_lldp_neighbors_single():
    output = """\
Local Port  Chassis ID             Port ID            System Name     Hold Time
----------  ---------------------  -----------------  ------------    ---------
eth1/0/5    AA-BB-CC-DD-EE-FF      ge0/0/1            Router-1        110

Total Entries: 1
"""
    result = parse_lldp_neighbors(output)
    assert len(result) == 1
    assert result[0]["local_port"] == "eth1/0/5"
    assert result[0]["port_id"] == "ge0/0/1"


def test_parse_lldp_neighbors_empty():
    result = parse_lldp_neighbors("")
    assert result == []


# ---------------------------------------------------------------------------
# parse_stp
# ---------------------------------------------------------------------------

SHOW_SPANNING_TREE_OUTPUT = """\
Spanning Tree Mode : RSTP
Spanning Tree State : Enabled

Root Bridge Information:
  Priority   : 32768
  MAC Address: F0-7D-68-12-50-01
  Hello Time : 2
  Max Age    : 20
  Forward Delay : 15

Bridge Information:
  Priority   : 32768
  MAC Address: F0-7D-68-12-50-01
  Hello Time : 2
  Max Age    : 20
  Forward Delay : 15
"""


def test_parse_stp_mode():
    result = parse_stp(SHOW_SPANNING_TREE_OUTPUT)
    assert result["mode"] == "RSTP"
    assert result["state"] == "Enabled"


def test_parse_stp_root():
    result = parse_stp(SHOW_SPANNING_TREE_OUTPUT)
    assert result["root"]["priority"] == 32768
    assert result["root"]["mac_address"] == "F0-7D-68-12-50-01"
    assert result["root"]["hello_time"] == 2
    assert result["root"]["max_age"] == 20
    assert result["root"]["forward_delay"] == 15


def test_parse_stp_bridge():
    result = parse_stp(SHOW_SPANNING_TREE_OUTPUT)
    assert result["bridge"]["priority"] == 32768
    assert result["bridge"]["mac_address"] == "F0-7D-68-12-50-01"
    assert result["bridge"]["hello_time"] == 2
    assert result["bridge"]["forward_delay"] == 15


def test_parse_stp_different_root():
    output = """\
Spanning Tree Mode : STP
Spanning Tree State : Enabled

Root Bridge Information:
  Priority   : 4096
  MAC Address: AA-BB-CC-DD-EE-FF
  Hello Time : 1
  Max Age    : 10
  Forward Delay : 8

Bridge Information:
  Priority   : 32768
  MAC Address: F0-7D-68-12-50-01
  Hello Time : 2
  Max Age    : 20
  Forward Delay : 15
"""
    result = parse_stp(output)
    assert result["mode"] == "STP"
    assert result["root"]["priority"] == 4096
    assert result["root"]["mac_address"] == "AA-BB-CC-DD-EE-FF"
    assert result["bridge"]["priority"] == 32768


def test_parse_stp_disabled():
    output = """\
Spanning Tree Mode : RSTP
Spanning Tree State : Disabled
"""
    result = parse_stp(output)
    assert result["state"] == "Disabled"
    assert result["root"] == {}
    assert result["bridge"] == {}


def test_parse_stp_empty():
    result = parse_stp("")
    assert result["mode"] == ""
    assert result["state"] == ""
    assert result["root"] == {}
    assert result["bridge"] == {}


# ---------------------------------------------------------------------------
# parse_static_routes
# ---------------------------------------------------------------------------

SHOW_IP_ROUTE_STATIC_OUTPUT = """\
Codes: C - Connected, S - Static, R - RIP, O - OSPF

S    10.0.0.0/24 [1] via 192.168.1.1
S    172.16.0.0/16 [10] via 192.168.1.1
S    10.10.0.0/16 [1] via 10.0.0.254

Total Routes: 3
"""


def test_parse_static_routes():
    result = parse_static_routes(SHOW_IP_ROUTE_STATIC_OUTPUT)
    assert len(result) == 3
    assert result[0]["prefix"] == "10.0.0.0"
    assert result[0]["prefix_length"] == 24
    assert result[0]["metric"] == 1
    assert result[0]["next_hop"] == "192.168.1.1"


def test_parse_static_routes_second():
    result = parse_static_routes(SHOW_IP_ROUTE_STATIC_OUTPUT)
    assert result[1]["prefix"] == "172.16.0.0"
    assert result[1]["prefix_length"] == 16
    assert result[1]["metric"] == 10


def test_parse_static_routes_third():
    result = parse_static_routes(SHOW_IP_ROUTE_STATIC_OUTPUT)
    assert result[2]["prefix"] == "10.10.0.0"
    assert result[2]["next_hop"] == "10.0.0.254"


def test_parse_static_routes_ignores_connected():
    output = """\
Codes: C - Connected, S - Static

C    192.168.1.0/24 is directly connected, VLAN1
S    10.0.0.0/24 [1] via 192.168.1.1

Total Routes: 2
"""
    result = parse_static_routes(output)
    assert len(result) == 1
    assert result[0]["prefix"] == "10.0.0.0"


def test_parse_static_routes_empty():
    result = parse_static_routes("")
    assert result == []
