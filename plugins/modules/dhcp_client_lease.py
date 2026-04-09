#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_client_lease
short_description: Configure DHCP client lease time on a D-Link DGS-1250 switch
description:
  - Configures the C(ip dhcp client lease) CLI command on a D-Link DGS-1250 switch.
  - Specifies the preferred lease time for the IP address requested from the DHCP server.
  - Corresponds to CLI command described in chapter 15-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.8.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - Interface on which to configure the DHCP client lease (e.g. C(vlan 100)).
    type: str
    required: true
  days:
    description:
      - Day duration of the lease (0-10000). Required when C(state=present).
    type: int
  hours:
    description:
      - Hour duration of the lease (0-23).
    type: int
  minutes:
    description:
      - Minute duration of the lease (0-59).
    type: int
  state:
    description:
      - C(present) to set the lease time, C(absent) to disable the lease option.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set DHCP client lease to 5 days on vlan 100
  jaydee_io.dlink_dgs1250.dhcp_client_lease:
    interface: vlan 100
    days: 5

- name: Set DHCP client lease to 1 day 12 hours 30 minutes on vlan 100
  jaydee_io.dlink_dgs1250.dhcp_client_lease:
    interface: vlan 100
    days: 1
    hours: 12
    minutes: 30

- name: Disable DHCP client lease option on vlan 100
  jaydee_io.dlink_dgs1250.dhcp_client_lease:
    interface: vlan 100
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


def _build_commands(interface, days, hours, minutes, state):
    """Build the CLI command list."""
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no ip dhcp client lease")
    else:
        cmd = "ip dhcp client lease %d" % days
        if hours is not None:
            cmd += " %d" % hours
            if minutes is not None:
                cmd += " %d" % minutes
        commands.append(cmd)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            days=dict(type="int"),
            hours=dict(type="int"),
            minutes=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["days"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"],
        module.params["days"],
        module.params["hours"],
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
