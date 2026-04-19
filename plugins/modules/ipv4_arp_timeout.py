#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv4_arp_timeout
short_description: Configure ARP timeout on an interface of a D-Link DGS-1250 switch
description:
  - Configures the C(arp timeout) CLI command on a D-Link DGS-1250 switch.
  - Sets or resets the ARP cache timeout on a specific interface.
  - Corresponds to CLI command described in chapter 9-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface on which to configure the ARP timeout (e.g. C(vlan1)).
    type: str
    required: true
  minutes:
    description:
      - ARP timeout value in minutes (0-65535). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the timeout, C(absent) to reset to default.
    type: str
    choices: [present, absent]
    default: present
notes:
"""

EXAMPLES = r"""
- name: Set ARP timeout to 60 minutes on vlan1
  jaydee_io.dlink_dgs1250.ipv4_arp_timeout:
    interface: vlan1
    minutes: 60

- name: Reset ARP timeout to default on vlan1
  jaydee_io.dlink_dgs1250.ipv4_arp_timeout:
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
        run_commands, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(interface, minutes, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["interface %s" % interface, "no arp timeout", "exit"]
    return ["interface %s" % interface, "arp timeout %d" % minutes, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            minutes=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["minutes"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"],
        module.params["minutes"],
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
