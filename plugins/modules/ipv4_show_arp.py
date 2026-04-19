#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv4_show_arp
short_description: Display ARP table on a D-Link DGS-1250 switch
description:
  - Executes the C(show arp) CLI command on a D-Link DGS-1250 switch.
  - Returns a list of ARP entries with their type, IP address, hardware address, interface, and age.
  - Corresponds to CLI command described in chapter 9-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  arp_type:
    description:
      - Filter by ARP entry type.
    type: str
    choices: [dynamic, static]
  ip_address:
    description:
      - Filter by IP address.
    type: str
  mask:
    description:
      - Subnet mask to use with C(ip_address) filter.
    type: str
  interface:
    description:
      - Filter by interface (e.g. C(vlan1)).
    type: str
  hardware_address:
    description:
      - Filter by hardware (MAC) address.
    type: str
"""

EXAMPLES = r"""
- name: Show all ARP entries
  jaydee_io.dlink_dgs1250.ipv4_show_arp:
  register: result

- name: Show only static ARP entries
  jaydee_io.dlink_dgs1250.ipv4_show_arp:
    arp_type: static
  register: result

- name: Show ARP entries for a specific interface
  jaydee_io.dlink_dgs1250.ipv4_show_arp:
    interface: vlan1
  register: result
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
entries:
  description: List of ARP entries.
  returned: success
  type: list
  elements: dict
  contains:
    static:
      description: Whether the entry is a static ARP entry.
      type: bool
    ip_address:
      description: IP address of the entry.
      type: str
    hardware_address:
      description: Hardware (MAC) address.
      type: str
    interface:
      description: Interface name.
      type: str
    age:
      description: Age of the entry.
      type: str
total_entries:
  description: Total number of ARP entries.
  returned: success
  type: int
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import run_command
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _parse_arp(output):
    """Parse the show arp output and return (entries, total)."""
    entries = []
    for line in output.splitlines():
        m = re.match(r"^(S?)\s+(\d+\.\d+\.\d+\.\d+)\s+(\S+)\s+(\S+)\s+(\S+)", line)
        if m:
            entries.append({
                "static": m.group(1) == "S",
                "ip_address": m.group(2),
                "hardware_address": m.group(3),
                "interface": m.group(4),
                "age": m.group(5),
            })
    total = 0
    m = re.search(r"Total Entries:\s*(\d+)", output)
    if m:
        total = int(m.group(1))
    return entries, total


def main():
    module = AnsibleModule(
        argument_spec=dict(
            arp_type=dict(type="str", choices=["dynamic", "static"]),
            ip_address=dict(type="str"),
            mask=dict(type="str"),
            interface=dict(type="str"),
            hardware_address=dict(type="str"),
        ),
        supports_check_mode=True,
    )

    cmd = "show arp"
    if module.params["arp_type"]:
        cmd += " %s" % module.params["arp_type"]
    if module.params["ip_address"]:
        cmd += " %s" % module.params["ip_address"]
        if module.params["mask"]:
            cmd += " %s" % module.params["mask"]
    if module.params["interface"]:
        cmd += " %s" % module.params["interface"]
    if module.params["hardware_address"]:
        cmd += " %s" % module.params["hardware_address"]

    try:
        raw_output = run_command(module, cmd)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    entries, total = _parse_arp(raw_output)
    module.exit_json(changed=False, raw_output=raw_output, entries=entries, total_entries=total)


if __name__ == "__main__":
    main()
