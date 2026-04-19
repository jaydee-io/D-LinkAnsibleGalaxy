#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_show_neighbors
short_description: Display IPv6 neighbor table on a D-Link DGS-1250 switch
description:
  - Executes the C(show ipv6 neighbors) CLI command on a D-Link DGS-1250 switch.
  - Returns a list of IPv6 neighbor entries with their address, link-layer address, interface, type, and state.
  - Corresponds to CLI command described in chapter 10-17 of the DGS-1250 CLI Reference Guide.
version_added: "0.7.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Filter by interface (e.g. C(vlan1)).
    type: str
  ipv6_address:
    description:
      - Filter by IPv6 address.
    type: str
"""

EXAMPLES = r"""
- name: Show all IPv6 neighbors
  jaydee_io.dlink_dgs1250.ipv6_show_neighbors:
  register: result

- name: Show IPv6 neighbors for vlan1
  jaydee_io.dlink_dgs1250.ipv6_show_neighbors:
    interface: vlan1
  register: result

- name: Show a specific IPv6 neighbor
  jaydee_io.dlink_dgs1250.ipv6_show_neighbors:
    ipv6_address: 2001:db8::1
  register: result
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
entries:
  description: List of IPv6 neighbor entries.
  returned: success
  type: list
  elements: dict
  contains:
    ipv6_address:
      description: IPv6 address of the neighbor.
      type: str
    link_layer_addr:
      description: Link-layer (MAC) address of the neighbor.
      type: str
    interface:
      description: Interface name.
      type: str
    type:
      description: Entry type (e.g. Static, Dynamic).
      type: str
    state:
      description: Neighbor state (e.g. REACH, STALE).
      type: str
total_entries:
  description: Total number of IPv6 neighbor entries.
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


def _parse_neighbors(output):
    """Parse the show ipv6 neighbors output and return (entries, total)."""
    entries = []
    for line in output.splitlines():
        m = re.match(
            r"^\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$",
            line,
        )
        if m:
            # Skip header lines
            if m.group(1).lower() == "ipv6" or m.group(1).startswith("-"):
                continue
            entries.append({
                "ipv6_address": m.group(1),
                "link_layer_addr": m.group(2),
                "interface": m.group(3),
                "type": m.group(4),
                "state": m.group(5),
            })
    total = 0
    m = re.search(r"Total Entries:\s*(\d+)", output)
    if m:
        total = int(m.group(1))
    return entries, total


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
            ipv6_address=dict(type="str"),
        ),
        supports_check_mode=True,
    )

    cmd = "show ipv6 neighbors"
    if module.params["interface"]:
        cmd += " %s" % module.params["interface"]
    if module.params["ipv6_address"]:
        cmd += " %s" % module.params["ipv6_address"]

    try:
        raw_output = run_command(module, cmd)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    entries, total = _parse_neighbors(raw_output)
    module.exit_json(changed=False, raw_output=raw_output, entries=entries, total_entries=total)


if __name__ == "__main__":
    main()
