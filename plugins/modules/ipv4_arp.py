#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv4_arp
short_description: Configure a static ARP entry on a D-Link DGS-1250 switch
description:
  - Configures the C(arp) CLI command on a D-Link DGS-1250 switch.
  - Creates or removes a static ARP entry mapping an IP address to a hardware (MAC) address.
  - Corresponds to CLI command described in chapter 9-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  ip_address:
    description:
      - IP address for the static ARP entry.
    type: str
    required: true
  hardware_address:
    description:
      - Hardware (MAC) address for the static ARP entry.
    type: str
    required: true
  state:
    description:
      - C(present) to create the entry, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
"""

EXAMPLES = r"""
- name: Add a static ARP entry
  jaydee_io.dlink_dgs1250.ipv4_arp:
    ip_address: 10.0.0.1
    hardware_address: 00-11-22-33-44-55

- name: Remove a static ARP entry
  jaydee_io.dlink_dgs1250.ipv4_arp:
    ip_address: 10.0.0.1
    hardware_address: 00-11-22-33-44-55
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


def _build_commands(ip_address, hardware_address, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no arp %s %s" % (ip_address, hardware_address)]
    return ["arp %s %s" % (ip_address, hardware_address)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip_address=dict(type="str", required=True),
            hardware_address=dict(type="str", required=True),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["ip_address"],
        module.params["hardware_address"],
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
