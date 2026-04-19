#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: poe_power_inline
short_description: Configure PoE power management mode on an interface on a D-Link DGS-1250 switch
description:
  - Configures the C(poe power-inline) CLI command on a D-Link DGS-1250 switch.
  - Sets the power management mode (auto/never) for a PoE port, optionally with a max wattage and time range.
  - Corresponds to CLI command described in chapter 51-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The PoE interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  mode:
    description:
      - The power management mode. Required when C(state=present).
    type: str
    choices: [auto, never]
  max_wattage:
    description:
      - Maximum wattage (mW) from 1000 to 30000. Only valid when C(mode=auto).
    type: int
  time_range:
    description:
      - Time-range profile name to activate the port. Only valid when C(mode=auto).
    type: str
  state:
    description:
      - C(present) to set the mode, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
  - Only applies to DGS-1250-28XMP and DGS-1250-52XMP models.
"""

EXAMPLES = r"""
- name: Enable auto PoE on port 1
  jaydee_io.dlink_dgs1250.poe_power_inline:
    interface: eth1/0/1
    mode: auto

- name: Enable auto with max wattage
  jaydee_io.dlink_dgs1250.poe_power_inline:
    interface: eth1/0/1
    mode: auto
    max_wattage: 7000

- name: Disable PoE on port 1
  jaydee_io.dlink_dgs1250.poe_power_inline:
    interface: eth1/0/1
    mode: never

- name: Revert to default
  jaydee_io.dlink_dgs1250.poe_power_inline:
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


def _build_commands(interface, mode, max_wattage, time_range, state):
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no poe power-inline")
    elif mode == "never":
        commands.append("poe power-inline never")
    else:
        cmd = "poe power-inline auto"
        if max_wattage is not None:
            cmd += " max %d" % max_wattage
        if time_range:
            cmd += " time-range %s" % time_range
        commands.append(cmd)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            mode=dict(type="str", choices=["auto", "never"]),
            max_wattage=dict(type="int"),
            time_range=dict(type="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["mode"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["mode"],
        module.params["max_wattage"],
        module.params["time_range"],
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
