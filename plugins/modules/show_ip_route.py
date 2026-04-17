#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_ip_route
short_description: Display the IPv4 routing table on a D-Link DGS-1250 switch
description:
  - Executes the C(show ip route) CLI command on a D-Link DGS-1250 switch.
  - Displays the IPv4 routing table entries, optionally filtered.
  - Corresponds to CLI command described in chapter 53-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil
options:
  ip_address:
    description:
      - Network address to filter by.
    type: str
  mask:
    description:
      - Subnet mask to use with C(ip_address).
    type: str
  filter_type:
    description:
      - Filter type to restrict the output.
    type: str
    choices: [connected, static, hardware]
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display the full routing table
  jaydee_io.dlink_dgs1250.show_ip_route:
  register: result

- name: Display only static routes
  jaydee_io.dlink_dgs1250.show_ip_route:
    filter_type: static
  register: result

- name: Display a specific network
  jaydee_io.dlink_dgs1250.show_ip_route:
    ip_address: 10.0.0.0
    mask: 255.0.0.0
  register: result
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
commands:
  description: List of CLI commands sent to the switch.
  returned: always
  type: list
  elements: str
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import (
        run_command,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(ip_address, mask, filter_type):
    cmd = "show ip route"
    if ip_address:
        cmd += " %s" % ip_address
        if mask:
            cmd += " %s" % mask
    elif filter_type:
        cmd += " %s" % filter_type
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip_address=dict(type="str"),
            mask=dict(type="str"),
            filter_type=dict(type="str", choices=["connected", "static", "hardware"]),
        ),
        mutually_exclusive=[("ip_address", "filter_type")],
        supports_check_mode=True,
    )
    command = _build_command(
        module.params["ip_address"],
        module.params["mask"],
        module.params["filter_type"],
    )
    if module.check_mode:
        module.exit_json(changed=False, commands=[command], raw_output="")
        return
    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=False, raw_output=raw_output, commands=[command])


if __name__ == "__main__":
    main()
