#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_route
short_description: Configure a static IPv6 route on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 route) CLI command on a D-Link DGS-1250 switch.
  - Creates or removes a static IPv6 route entry.
  - Corresponds to CLI command described in chapter 53-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  network_prefix:
    description:
      - IPv6 destination prefix in the form C(PREFIX/LENGTH), or C(default) for the default route.
    type: str
    required: true
  interface:
    description:
      - Optional forwarding interface (e.g. C(vlan1)).
    type: str
  next_hop:
    description:
      - IPv6 address of the next hop.
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
- name: Add an IPv6 static route
  jaydee_io.dlink_dgs1250.ipv6_route:
    network_prefix: "2001:0101::/32"
    interface: vlan1
    next_hop: "fe80::ff:1111:2233"

- name: Add an IPv6 default route
  jaydee_io.dlink_dgs1250.ipv6_route:
    network_prefix: default
    next_hop: "2001::1"

- name: Remove an IPv6 static route
  jaydee_io.dlink_dgs1250.ipv6_route:
    network_prefix: "2001:0101::/32"
    interface: vlan1
    next_hop: "fe80::ff:1111:2233"
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
        run_commands, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(network_prefix, interface, next_hop, route_type, state):
    cmd = "ipv6 route %s" % network_prefix
    if interface:
        cmd += " %s" % interface
    cmd += " %s" % next_hop
    if state == "absent":
        return ["no " + cmd]
    if route_type:
        cmd += " %s" % route_type
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            network_prefix=dict(type="str", required=True),
            interface=dict(type="str"),
            next_hop=dict(type="str", required=True),
            route_type=dict(type="str", choices=["primary", "backup"]),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["network_prefix"],
        module.params["interface"],
        module.params["next_hop"],
        module.params["route_type"],
        module.params["state"],
    )
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
