"""
Structured output parsers for D-Link DGS-1250 CLI commands.
Used by dgs1250_facts and individual show_* modules.
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re


def parse_version(output):
    """Parse 'show version' output into a structured dict."""
    result = {
        "system_mac_address": "",
        "module_name": "",
        "hardware_version": "",
        "runtime": "",
    }
    for line in output.splitlines():
        m = re.match(r"^\s*System MAC Address:\s*(\S+)", line)
        if m:
            result["system_mac_address"] = m.group(1).strip()
            continue
        m = re.match(r"^\s*Module Name\s+(\S+)", line)
        if m:
            result["module_name"] = m.group(1).strip()
            continue
        m = re.match(r"^\s*H/W\s+(\S+)", line)
        if m:
            result["hardware_version"] = m.group(1).strip()
            continue
        m = re.match(r"^\s*Runtime\s+(\S+)", line)
        if m:
            result["runtime"] = m.group(1).strip()
            continue
    return result


def parse_unit(output):
    """Parse 'show unit' output into a structured dict."""
    model = {"model_description": "", "model_name": ""}
    in_section = False
    for line in output.splitlines():
        if "Model Descr" in line and "Model Name" in line:
            in_section = True
            continue
        if not in_section:
            continue
        if re.match(r"^[-\s]+$", line):
            continue
        m = re.match(r"^\s*(.+?)\s{2,}(\S+)\s*$", line)
        if m:
            model["model_description"] = m.group(1).strip()
            model["model_name"] = m.group(2).strip()
            break

    unit_info = {
        "serial_number": "", "status": "",
        "uptime": {"days": 0, "hours": 0, "minutes": 0, "seconds": 0},
        "uptime_raw": 0,
    }
    in_section = False
    for line in output.splitlines():
        if "Serial-Number" in line and "Status" in line:
            in_section = True
            continue
        if not in_section:
            continue
        if re.match(r"^[-\s]+$", line):
            continue
        m = re.match(r"^\s*(\S+)\s{2,}(\S+)\s{2,}(\S+)\s*$", line)
        if m:
            unit_info["serial_number"] = m.group(1).strip()
            unit_info["status"] = m.group(2).strip()
            uptime_m = re.match(
                r"(\d+)DT(\d+)H(\d+)M(\d+)S", m.group(3).strip())
            if uptime_m:
                unit_info["uptime"] = {
                    "days": int(uptime_m.group(1)),
                    "hours": int(uptime_m.group(2)),
                    "minutes": int(uptime_m.group(3)),
                    "seconds": int(uptime_m.group(4)),
                }
                unit_info["uptime_raw"] = (
                    int(uptime_m.group(1)) * 86400
                    + int(uptime_m.group(2)) * 3600
                    + int(uptime_m.group(3)) * 60
                    + int(uptime_m.group(4))
                )
            break

    memory = []
    in_section = False
    for line in output.splitlines():
        if re.match(r"^\s*Memory\s+Total\s+Used\s+Free", line):
            in_section = True
            continue
        if not in_section:
            continue
        if re.match(r"^[-\s]+$", line):
            continue
        m = re.match(
            r"^\s*(DRAM|FLASH)\s+(\d+)\s*K\s+(\d+)\s*K\s+(\d+)\s*K\s*$", line
        )
        if m:
            memory.append({
                "type": m.group(1),
                "total_kb": int(m.group(2)),
                "used_kb": int(m.group(3)),
                "free_kb": int(m.group(4)),
            })

    return {"model": model, "unit": unit_info, "memory": memory}


def parse_environment(output):
    """Parse 'show environment' output into a structured dict."""
    temperatures = []
    in_section = False
    for line in output.splitlines():
        if "Detail Temperature Status" in line:
            in_section = True
            continue
        if in_section and line.startswith("Detail ") and "Temperature" not in line:
            break
        if not in_section:
            continue
        m = re.match(r"^(.+?)\s{2,}(\d+)C/(\d+)~(\d+)C\s*(\*?)\s*$", line)
        if m:
            current = int(m.group(2))
            thr_min = int(m.group(3))
            thr_max = int(m.group(4))
            temperatures.append({
                "name": m.group(1).strip(),
                "current_celsius": current,
                "threshold_min_celsius": thr_min,
                "threshold_max_celsius": thr_max,
                "out_of_range": bool(m.group(5)) or not (thr_min <= current <= thr_max),
            })

    fans = []
    in_section = False
    for line in output.splitlines():
        if "Detail Fan Status" in line:
            in_section = True
            continue
        if in_section and line.startswith("Detail ") and "Fan" not in line:
            break
        if not in_section:
            continue
        for m in re.finditer(r"([\w\s]+?)\s*\((OK|FAIL)\)", line):
            fans.append({"name": m.group(1).strip(), "status": m.group(2)})

    power = []
    in_section = False
    for line in output.splitlines():
        if "Detail Power Status" in line:
            in_section = True
            continue
        if in_section and line.startswith("Detail ") and "Power" not in line:
            break
        if not in_section:
            continue
        if re.match(r"^[-\s]+$", line):
            continue
        if line.strip().startswith("Power Module"):
            continue
        m = re.match(r"^(Power\s+\S+)\s{2,}(.+)$", line)
        if m:
            power.append({"module": m.group(1).strip(),
                         "status": m.group(2).strip()})

    return {"temperatures": temperatures, "fans": fans, "power": power}


def parse_cpu(output):
    """Parse 'show cpu utilization' output into a structured dict."""
    result = {
        "five_seconds_percent": 0,
        "one_minute_percent": 0,
        "five_minutes_percent": 0,
    }
    for line in output.splitlines():
        m = re.match(r"^\s*Five seconds\s*-\s*(\d+)\s*%", line, re.IGNORECASE)
        if m:
            result["five_seconds_percent"] = int(m.group(1))
            continue
        m = re.match(r"^\s*One minute\s*-\s*(\d+)\s*%", line, re.IGNORECASE)
        if m:
            result["one_minute_percent"] = int(m.group(1))
            continue
        m = re.match(r"^\s*Five minutes\s*-\s*(\d+)\s*%", line, re.IGNORECASE)
        if m:
            result["five_minutes_percent"] = int(m.group(1))
            continue
    return result


def parse_interfaces(output):
    """Parse 'show interfaces status' output into a list of dicts."""
    interfaces = []
    for line in output.splitlines():
        m = re.match(
            r"^\s*(eth\S+)\s+(connected|not-connected|disabled)\s+"
            r"(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$",
            line,
        )
        if m:
            interfaces.append({
                "port": m.group(1),
                "status": m.group(2),
                "vlan": m.group(3),
                "duplex": m.group(4),
                "speed": m.group(5),
                "type": m.group(6),
            })
    return interfaces


def parse_vlans(output):
    """Parse 'show vlan' output into a list of dicts."""
    vlans = []
    current = None
    for line in output.splitlines():
        m = re.match(r"^\s*VLAN\s+(\d+)\s*$", line)
        if m:
            if current is not None:
                vlans.append(current)
            current = {
                "vlan_id": int(m.group(1)),
                "name": "",
                "tagged_ports": "",
                "untagged_ports": "",
            }
            continue
        if current is None:
            continue
        m = re.match(r"^\s*Name\s*:\s*(.*?)\s*$", line)
        if m:
            current["name"] = m.group(1)
            continue
        m = re.match(r"^\s*Tagged Member Ports\s*:\s*(.*?)\s*$", line)
        if m:
            current["tagged_ports"] = m.group(1)
            continue
        m = re.match(r"^\s*Untagged Member Ports\s*:\s*(.*?)\s*$", line)
        if m:
            current["untagged_ports"] = m.group(1)
            continue
    if current is not None:
        vlans.append(current)
    return vlans


def parse_mac_table(output):
    """Parse 'show mac-address-table' output into a list of dicts."""
    entries = []
    for line in output.splitlines():
        m = re.match(
            r"^\s*(\d+)\s+([\dA-Fa-f]{2}(?:[-:][\dA-Fa-f]{2}){5})\s+"
            r"(Static|Dynamic)\s+(\S+)\s*$",
            line,
        )
        if m:
            entries.append({
                "vlan": int(m.group(1)),
                "mac_address": m.group(2),
                "type": m.group(3),
                "port": m.group(4),
            })
    return entries


def parse_snmp(output):
    """Parse 'show snmp community' output into a list of dicts."""
    communities = []
    for line in output.splitlines():
        m = re.match(
            r"^\s*(\S+)\s{2,}(\S+)\s{2,}(Read-Only|Read-Write)\s*$",
            line,
        )
        if m:
            communities.append({
                "community": m.group(1),
                "view": m.group(2),
                "access": m.group(3),
            })
    return communities


def parse_lldp_neighbors(output):
    """Parse 'show lldp neighbors' output into a list of dicts."""
    neighbors = []
    for line in output.splitlines():
        m = re.match(
            r"^\s*(eth\S+)\s{2,}"
            r"([\dA-Fa-f]{2}(?:[-:][\dA-Fa-f]{2}){5})\s{2,}"
            r"(\S+)\s{2,}"
            r"(.*?)\s{2,}"
            r"(\d+)\s*$",
            line,
        )
        if m:
            neighbors.append({
                "local_port": m.group(1),
                "chassis_id": m.group(2),
                "port_id": m.group(3),
                "system_name": m.group(4).strip(),
                "hold_time": int(m.group(5)),
            })
    return neighbors


def parse_stp(output):
    """Parse 'show spanning-tree' output into a structured dict."""
    result = {
        "mode": "",
        "state": "",
        "root": {},
        "bridge": {},
    }
    for line in output.splitlines():
        m = re.match(r"^\s*Spanning Tree Mode\s*:\s*(.+?)\s*$", line)
        if m:
            result["mode"] = m.group(1)
            continue
        m = re.match(r"^\s*Spanning Tree State\s*:\s*(.+?)\s*$", line)
        if m:
            result["state"] = m.group(1)
            continue

    for section_key, section_re in [("root", r"Root Bridge Information"),
                                    ("bridge", r"(?<!Root )Bridge Information")]:
        in_section = False
        info = {}
        for line in output.splitlines():
            if re.search(section_re, line):
                in_section = True
                continue
            if in_section and line.strip() == "":
                if info:
                    break
                continue
            if not in_section:
                continue
            m = re.match(r"^\s*Priority\s*:\s*(\d+)", line)
            if m:
                info["priority"] = int(m.group(1))
                continue
            m = re.match(r"^\s*MAC Address\s*:\s*(\S+)", line)
            if m:
                info["mac_address"] = m.group(1)
                continue
            m = re.match(r"^\s*Hello Time\s*:\s*(\d+)", line)
            if m:
                info["hello_time"] = int(m.group(1))
                continue
            m = re.match(r"^\s*Max Age\s*:\s*(\d+)", line)
            if m:
                info["max_age"] = int(m.group(1))
                continue
            m = re.match(r"^\s*Forward Delay\s*:\s*(\d+)", line)
            if m:
                info["forward_delay"] = int(m.group(1))
                continue
        if info:
            result[section_key] = info

    return result


def parse_static_routes(output):
    """Parse 'show ip route static' output into a list of dicts."""
    routes = []
    for line in output.splitlines():
        m = re.match(
            r"^\s*S\s+(\S+)/(\d+)\s+\[(\d+)\]\s+via\s+(\S+)\s*$",
            line,
        )
        if m:
            routes.append({
                "prefix": m.group(1),
                "prefix_length": int(m.group(2)),
                "metric": int(m.group(3)),
                "next_hop": m.group(4),
            })
    return routes
