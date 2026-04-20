#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: snmp_environment_traps
short_description: Enable or disable environment SNMP traps on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server enable traps environment) command on a D-Link DGS-1250 switch.
  - Enables or disables SNMP traps for fan, power, and temperature events.
  - Corresponds to CLI command described in chapter 2-14 of the DGS-1250 CLI Reference Guide.
version_added: "0.1.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  state:
    description:
      - Whether environment traps should be enabled or disabled.
    type: str
    choices: [enabled, disabled]
    default: enabled
  fan:
    description:
      - Enable or disable the fan trap state for warning fan events (fan failed or fan recover).
      - If none of C(fan), C(power), C(temperature) are specified, all traps are affected.
    type: bool
    default: false
  power:
    description:
      - Enable or disable the power trap state for warning power events (power failure or power recovery).
      - If none of C(fan), C(power), C(temperature) are specified, all traps are affected.
    type: bool
    default: false
  temperature:
    description:
      - Enable or disable the temperature trap state for warning temperature events.
      - If none of C(fan), C(power), C(temperature) are specified, all traps are affected.
    type: bool
    default: false
notes:
  - This command requires Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable all environment traps
  jaydee_io.dlink_dgs1250.snmp_environment_traps:
    state: enabled

- name: Enable only fan and temperature traps
  jaydee_io.dlink_dgs1250.snmp_environment_traps:
    state: enabled
    fan: true
    temperature: true

- name: Disable all environment traps
  jaydee_io.dlink_dgs1250.snmp_environment_traps:
    state: disabled
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

def _build_command(state, fan, power, temperature):
    """Build the CLI command string."""
    prefix = "" if state == "enabled" else "no "
    cmd = prefix + "snmp-server enable traps environment"

    components = []
    if fan:
        components.append("fan")
    if power:
        components.append("power")
    if temperature:
        components.append("temperature")

    if components:
        cmd += " " + " ".join(components)

    return cmd


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", choices=[
                       "enabled", "disabled"], default="enabled"),
            fan=dict(type="bool", default=False),
            power=dict(type="bool", default=False),
            temperature=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )

    state = module.params["state"]
    fan = module.params["fan"]
    power = module.params["power"]
    temperature = module.params["temperature"]

    command = _build_command(state, fan, power, temperature)
    commands = [command]

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
