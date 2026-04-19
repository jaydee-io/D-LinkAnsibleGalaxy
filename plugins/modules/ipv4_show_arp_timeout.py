#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv4_show_arp_timeout
short_description: Display ARP timeout settings on a D-Link DGS-1250 switch
description:
  - Executes the C(show arp timeout) CLI command on a D-Link DGS-1250 switch.
  - Returns the ARP timeout configuration for each interface.
  - Corresponds to CLI command described in chapter 9-6 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface to query (e.g. C(vlan1)). If omitted, all interfaces are shown.
    type: str
notes:
"""

EXAMPLES = r"""
- name: Show ARP timeout for all interfaces
  jaydee_io.dlink_dgs1250.ipv4_show_arp_timeout:
  register: result

- name: Show ARP timeout for vlan1
  jaydee_io.dlink_dgs1250.ipv4_show_arp_timeout:
    interface: vlan1
  register: result
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
entries:
  description: List of interface ARP timeout entries.
  returned: success
  type: list
  elements: dict
  contains:
    interface:
      description: Interface name.
      type: str
    timeout:
      description: ARP timeout in minutes.
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


def _parse_arp_timeout(output):
    """Parse the show arp timeout output and return a list of entries."""
    entries = []
    for line in output.splitlines():
        m = re.match(r"^\s*(\S+)\s+(\d+)\s*$", line)
        if m:
            entries.append({
                "interface": m.group(1),
                "timeout": int(m.group(2)),
            })
    return entries


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
        ),
        supports_check_mode=True,
    )

    cmd = "show arp timeout"
    if module.params["interface"]:
        cmd += " interface %s" % module.params["interface"]

    try:
        raw_output = run_command(module, cmd)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    entries = _parse_arp_timeout(raw_output)
    module.exit_json(changed=False, raw_output=raw_output, entries=entries)


if __name__ == "__main__":
    main()
