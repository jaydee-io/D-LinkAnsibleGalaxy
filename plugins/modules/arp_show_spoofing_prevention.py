#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: arp_show_spoofing_prevention
short_description: Display ARP spoofing prevention entries on a D-Link DGS-1250 switch
description:
  - Executes the C(show ip arp spoofing-prevention) CLI command on a D-Link DGS-1250 switch.
  - Returns a list of configured ARP spoofing prevention entries.
  - Corresponds to CLI command described in chapter 6-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.5.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options: {}
"""

EXAMPLES = r"""
- name: Show ARP spoofing prevention entries
  jaydee_io.dlink_dgs1250.arp_show_spoofing_prevention:
  register: result
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
entries:
  description: List of ARP spoofing prevention entries.
  returned: success
  type: list
  elements: dict
  contains:
    ip:
      description: Gateway IP address.
      type: str
    mac:
      description: Gateway MAC address.
      type: str
    interfaces:
      description: Interfaces on which the entry is active.
      type: str
total_entries:
  description: Total number of entries.
  returned: success
  type: int
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import run_command
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _parse_entries(output):
    entries = []
    for line in output.splitlines():
        m = re.match(r"^\s*(\d+\.\d+\.\d+\.\d+)\s+(\S+)\s+(.+)", line)
        if m:
            entries.append({
                "ip": m.group(1),
                "mac": m.group(2),
                "interfaces": m.group(3).strip(),
            })
    total = 0
    m = re.search(r"Total Entries:\s*(\d+)", output)
    if m:
        total = int(m.group(1))
    return entries, total


def main():
    module = AnsibleModule(argument_spec=dict(), supports_check_mode=True)

    try:
        raw_output = run_command(module, "show ip arp spoofing-prevention")
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    entries, total = _parse_entries(raw_output)
    module.exit_json(changed=False, raw_output=raw_output,
                     entries=entries, total_entries=total)


if __name__ == "__main__":
    main()
