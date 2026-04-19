#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_source_binding
short_description: Configure a static IPv6 source binding entry on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 source binding) CLI command on a D-Link DGS-1250 switch.
  - Adds or removes a static entry in the IPv6 binding table.
  - Corresponds to CLI command described in chapter 38-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.13.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  mac_address:
    description:
      - The MAC address of the manual binding entry.
    type: str
    required: true
  vlan_id:
    description:
      - The binding VLAN of the manual binding entry.
    type: int
    required: true
  ipv6_address:
    description:
      - The IPv6 address of the manual binding entry.
    type: str
    required: true
  interface:
    description:
      - The interface number of the manual binding entry (e.g. C(eth1/0/1)).
    type: str
    required: true
  state:
    description:
      - C(present) to add the binding, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Add a static IPv6 source binding
  jaydee_io.dlink_dgs1250.ipv6_source_binding:
    mac_address: 00-01-02-03-04-05
    vlan_id: 2
    ipv6_address: "2000::1"
    interface: eth1/0/1

- name: Remove a static IPv6 source binding
  jaydee_io.dlink_dgs1250.ipv6_source_binding:
    mac_address: 00-01-02-03-04-05
    vlan_id: 2
    ipv6_address: "2000::1"
    interface: eth1/0/1
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(mac_address, vlan_id, ipv6_address, interface, state):
    """Build the CLI command list."""
    base = "ipv6 source binding %s vlan %d %s interface %s" % (
        mac_address, vlan_id, ipv6_address, interface
    )
    if state == "absent":
        return ["no %s" % base]
    return [base]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            mac_address=dict(type="str", required=True),
            vlan_id=dict(type="int", required=True),
            ipv6_address=dict(type="str", required=True),
            interface=dict(type="str", required=True),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["mac_address"],
        module.params["vlan_id"],
        module.params["ipv6_address"],
        module.params["interface"],
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
