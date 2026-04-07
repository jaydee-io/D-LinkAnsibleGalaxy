#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dot1x_port_control
short_description: Configure 802.1X port authorization state on a D-Link DGS-1250 switch
description:
  - Configures the C(dot1x port-control) CLI command on a D-Link DGS-1250 switch.
  - Controls the authorization state of a port (auto, force-authorized, force-unauthorized).
  - Use C(state=absent) to revert to the default setting (auto).
  - Corresponds to CLI command described in chapter 3-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.2.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - Physical port interface to configure (e.g. C(eth1/0/1)).
    required: true
    type: str
  control:
    description:
      - Port authorization state.
      - C(auto) enables 802.1X authentication for the port.
      - C(force-authorized) forces the port to the authorized state.
      - C(force-unauthorized) forces the port to the unauthorized state.
    type: str
    choices: [auto, force-authorized, force-unauthorized]
  state:
    description:
      - Whether to set (C(present)) or reset to default (C(absent)) the port control.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Interface Configuration Mode.
  - Takes effect only when 802.1X PAE authenticator is globally enabled.
"""

EXAMPLES = r"""
- name: Deny all access on port 1
  jaydee_io.dlink_dgs1250.dot1x_port_control:
    interface: eth1/0/1
    control: force-unauthorized

- name: Force authorize port 1
  jaydee_io.dlink_dgs1250.dot1x_port_control:
    interface: eth1/0/1
    control: force-authorized

- name: Reset to default (auto)
  jaydee_io.dlink_dgs1250.dot1x_port_control:
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
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(interface, state, control):
    """Build the CLI command list for interface configuration."""
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no dot1x port-control")
    else:
        commands.append("dot1x port-control %s" % control)
    return commands


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            control=dict(type="str", choices=["auto", "force-authorized", "force-unauthorized"]),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["control"]),
        ],
        supports_check_mode=True,
    )

    interface = module.params["interface"]
    state = module.params["state"]
    control = module.params["control"]

    commands = _build_commands(interface, state, control)

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
