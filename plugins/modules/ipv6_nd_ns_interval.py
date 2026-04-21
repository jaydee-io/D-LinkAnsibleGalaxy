#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_nd_ns_interval
short_description: Configure IPv6 ND neighbor solicitation interval on an interface of a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 nd ns-interval) CLI command on a D-Link DGS-1250 switch.
  - Sets or resets the neighbor solicitation retransmit interval advertised in router advertisements.
  - Corresponds to CLI command described in chapter 10-14 of the DGS-1250 CLI Reference Guide.
version_added: "0.7.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface on which to configure the NS interval (e.g. C(vlan1)).
    type: str
    required: true
  milliseconds:
    description:
      - Neighbor solicitation interval in milliseconds (0-3600000). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the interval, C(absent) to reset to default.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Set ND NS interval to 1000 ms on vlan1
  jaydee_io.dlink_dgs1250.ipv6_nd_ns_interval:
    interface: vlan1
    milliseconds: 1000

- name: Reset ND NS interval to default on vlan1
  jaydee_io.dlink_dgs1250.ipv6_nd_ns_interval:
    interface: vlan1
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
        run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG


def _build_commands(interface, milliseconds, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["interface %s" % interface, "no ipv6 nd ns-interval", "exit"]
    return ["interface %s" % interface, "ipv6 nd ns-interval %d" % milliseconds, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            milliseconds=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["milliseconds"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"],
        module.params["milliseconds"],
        module.params["state"],
    )

    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
    diff = build_config_diff(module, commands) if module._diff else None
    if module.check_mode:
        result = dict(changed=True, commands=commands, raw_output="")
        if diff:
            result['diff'] = diff
        module.exit_json(**result)
        return

    try:
        raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    result = dict(changed=True, raw_output=raw_output, commands=commands)
    if diff:
        result['diff'] = diff
    module.exit_json(**result)


if __name__ == "__main__":
    main()
