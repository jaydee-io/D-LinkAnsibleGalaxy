#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: snmp_environment_traps
short_description: Enable or disable environment SNMP traps on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server enable traps environment) command on a D-Link DGS-1250 switch via SSH.
  - Enables or disables SNMP traps for fan, power, and temperature events.
  - Corresponds to CLI command described in chapter 2-14 of the DGS-1250 CLI Reference Guide.
version_added: "0.1.0"
author:
  - Jérôme Dumesnil
options:
  host:
    description: IP address or hostname of the switch.
    required: true
    type: str
  username:
    description: SSH username.
    required: true
    type: str
  password:
    description: SSH password.
    required: true
    type: str
    no_log: true
  port:
    description: SSH port.
    type: int
    default: 22
  timeout:
    description: SSH connection timeout in seconds.
    type: int
    default: 30
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
  - Requires C(paramiko) on the Ansible controller (C(pip install paramiko)).
  - The switch must be reachable via SSH from the Ansible controller.
  - This command requires Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable all environment traps
  dlink.dgs1250.snmp_environment_traps:
    host: 192.168.1.1
    username: admin
    password: admin
    state: enabled

- name: Enable only fan and temperature traps
  dlink.dgs1250.snmp_environment_traps:
    host: 192.168.1.1
    username: admin
    password: admin
    state: enabled
    fan: true
    temperature: true

- name: Disable all environment traps
  dlink.dgs1250.snmp_environment_traps:
    host: 192.168.1.1
    username: admin
    password: admin
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
    from ansible_collections.dlink.dgs1250.plugins.module_utils.dgs1250 import (
        DGS1250Connection,
        HAS_PARAMIKO,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import DGS1250Connection, HAS_PARAMIKO


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
            host=dict(type="str", required=True),
            username=dict(type="str", required=True),
            password=dict(type="str", required=True, no_log=True),
            port=dict(type="int", default=22),
            timeout=dict(type="int", default=30),
            state=dict(type="str", choices=["enabled", "disabled"], default="enabled"),
            fan=dict(type="bool", default=False),
            power=dict(type="bool", default=False),
            temperature=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )

    if not HAS_PARAMIKO:
        module.fail_json(msg="paramiko is required: pip install paramiko")

    host = module.params["host"]
    username = module.params["username"]
    password = module.params["password"]
    port = module.params["port"]
    timeout = module.params["timeout"]
    state = module.params["state"]
    fan = module.params["fan"]
    power = module.params["power"]
    temperature = module.params["temperature"]

    command = _build_command(state, fan, power, temperature)
    commands = ["configure terminal", command]

    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return

    try:
        with DGS1250Connection(host, username, password, port, timeout) as conn:
            raw_output = ""
            for cmd in commands:
                raw_output += conn.send_command(cmd) + "\n"
    except Exception as e:
        module.fail_json(msg="SSH connection or command failed: %s" % str(e))

    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
