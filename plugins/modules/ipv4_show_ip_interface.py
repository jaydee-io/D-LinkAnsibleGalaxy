#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv4_show_ip_interface
short_description: Display IP interface information on a D-Link DGS-1250 switch
description:
  - Executes the C(show ip interface) CLI command on a D-Link DGS-1250 switch.
  - Returns IP interface configuration including addresses and status.
  - Corresponds to CLI command described in chapter 9-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - Interface to query (e.g. C(vlan1)). If omitted, all interfaces are shown.
    type: str
  brief:
    description:
      - When C(true), show brief output format.
    type: bool
    default: false
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
"""

EXAMPLES = r"""
- name: Show all IP interfaces (brief)
  jaydee_io.dlink_dgs1250.ipv4_show_ip_interface:
    brief: true
  register: result

- name: Show IP interface for vlan1
  jaydee_io.dlink_dgs1250.ipv4_show_ip_interface:
    interface: vlan1
    brief: true
  register: result
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
entries:
  description: List of IP interface entries.
  returned: success
  type: list
  elements: dict
  contains:
    interface:
      description: Interface name.
      type: str
    ip_address:
      description: IP address assigned to the interface.
      type: str
    subnet_mask:
      description: Subnet mask.
      type: str
    admin_status:
      description: Administrative status (Up/Down).
      type: str
    oper_status:
      description: Operational status (Up/Down).
      type: str
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import run_command
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _parse_ip_interface(output):
    """Parse the show ip interface brief output and return a list of entries."""
    entries = []
    for line in output.splitlines():
        m = re.match(
            r"^\s*(\S+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\S+)\s+(\S+)\s*$",
            line,
        )
        if m:
            entries.append({
                "interface": m.group(1),
                "ip_address": m.group(2),
                "subnet_mask": m.group(3),
                "admin_status": m.group(4),
                "oper_status": m.group(5),
            })
    return entries


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
            brief=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )

    cmd = "show ip interface"
    if module.params["interface"]:
        cmd += " %s" % module.params["interface"]
    if module.params["brief"]:
        cmd += " brief"

    try:
        raw_output = run_command(module, cmd)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    entries = _parse_ip_interface(raw_output)
    module.exit_json(changed=False, raw_output=raw_output, entries=entries)


if __name__ == "__main__":
    main()
