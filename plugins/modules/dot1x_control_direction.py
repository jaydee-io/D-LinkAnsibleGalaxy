#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dot1x_control_direction
short_description: Configure 802.1X traffic control direction on a D-Link DGS-1250 switch port
description:
  - Configures the C(dot1x control-direction) CLI command on a D-Link DGS-1250 switch.
  - Sets the direction of traffic on a controlled port as unidirectional (in) or bidirectional (both).
  - Use C(state=absent) to revert to the default setting (bidirectional).
  - Corresponds to CLI command described in chapter 3-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.2.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Physical port interface to configure (e.g. C(eth1/0/1)).
    required: true
    type: str
  direction:
    description:
      - Traffic control direction.
      - C(both) for bidirectional control, C(in) for unidirectional (ingress only).
    type: str
    choices: [both, in]
  state:
    description:
      - Whether to set (C(present)) or reset to default (C(absent)) the control direction.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
  - The C(in) direction is only valid when multi-host mode is configured.
"""

EXAMPLES = r"""
- name: Set unidirectional control on port 1
  jaydee_io.dlink_dgs1250.dot1x_control_direction:
    interface: eth1/0/1
    direction: in

- name: Set bidirectional control on port 1
  jaydee_io.dlink_dgs1250.dot1x_control_direction:
    interface: eth1/0/1
    direction: both

- name: Reset to default (bidirectional)
  jaydee_io.dlink_dgs1250.dot1x_control_direction:
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
        run_commands, is_config_present, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, MODE_GLOBAL_CONFIG


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(interface, state, direction):
    """Build the CLI command list for interface configuration."""
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no dot1x control-direction")
    else:
        commands.append("dot1x control-direction %s" % direction)
    return commands


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            direction=dict(type="str", choices=["both", "in"]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["direction"]),
        ],
        supports_check_mode=True,
    )

    interface = module.params["interface"]
    state = module.params["state"]
    direction = module.params["direction"]

    commands = _build_commands(interface, state, direction)

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
