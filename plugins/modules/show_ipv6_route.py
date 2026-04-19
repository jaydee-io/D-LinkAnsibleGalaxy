#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_ipv6_route
short_description: Display the IPv6 routing table on a D-Link DGS-1250 switch
description:
  - Executes the C(show ipv6 route) CLI command on a D-Link DGS-1250 switch.
  - Displays the IPv6 routing table entries, optionally filtered.
  - Corresponds to CLI command described in chapter 53-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  filter_type:
    description:
      - Filter type (C(connected) or C(static)).
    type: str
    choices: [connected, static]
  database:
    description:
      - Display all related entries in the routing database instead of just the best route.
    type: bool
    default: false
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Show IPv6 routing table
  jaydee_io.dlink_dgs1250.show_ipv6_route:
  register: result

- name: Show IPv6 static routes
  jaydee_io.dlink_dgs1250.show_ipv6_route:
    filter_type: static
  register: result

- name: Show IPv6 routing database
  jaydee_io.dlink_dgs1250.show_ipv6_route:
    database: true
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(filter_type, database):
    cmd = "show ipv6 route"
    if filter_type:
        cmd += " %s" % filter_type
    if database:
        cmd += " database"
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            filter_type=dict(type="str", choices=["connected", "static"]),
            database=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )
    command = _build_command(
        module.params["filter_type"],
        module.params["database"],
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
