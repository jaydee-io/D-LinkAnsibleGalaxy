#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ip_route
short_description: Configure a static IPv4 route on a D-Link DGS-1250 switch
description:
  - Configures the C(ip route) CLI command on a D-Link DGS-1250 switch.
  - Creates or removes a static IPv4 route entry.
  - Corresponds to CLI command described in chapter 53-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  network_prefix:
    description:
      - Destination network address.
    type: str
    required: true
  network_mask:
    description:
      - Destination network mask.
    type: str
    required: true
  next_hop:
    description:
      - IP address of the next hop.
    type: str
    required: true
  route_type:
    description:
      - Specify the route as C(primary) or C(backup).
    type: str
    choices: [primary, backup]
  state:
    description:
      - C(present) to create the route, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Add a static route
  jaydee_io.dlink_dgs1250.ip_route:
    network_prefix: 20.0.0.0
    network_mask: 255.0.0.0
    next_hop: 10.1.1.254

- name: Add a backup route
  jaydee_io.dlink_dgs1250.ip_route:
    network_prefix: 20.0.0.0
    network_mask: 255.0.0.0
    next_hop: 10.1.1.254
    route_type: backup

- name: Remove a static route
  jaydee_io.dlink_dgs1250.ip_route:
    network_prefix: 20.0.0.0
    network_mask: 255.0.0.0
    next_hop: 10.1.1.254
    state: absent
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
        run_commands, is_config_present, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, MODE_GLOBAL_CONFIG


def _build_commands(network_prefix, network_mask, next_hop, route_type, state):
    cmd = "ip route %s %s %s" % (network_prefix, network_mask, next_hop)
    if state == "absent":
        return ["no " + cmd]
    if route_type:
        cmd += " %s" % route_type
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            network_prefix=dict(type="str", required=True),
            network_mask=dict(type="str", required=True),
            next_hop=dict(type="str", required=True),
            route_type=dict(type="str", choices=["primary", "backup"]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["network_prefix"],
        module.params["network_mask"],
        module.params["next_hop"],
        module.params["route_type"],
        module.params["state"],
    )
    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
