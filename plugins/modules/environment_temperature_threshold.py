#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: environment_temperature_threshold
short_description: Configure environment temperature thresholds on a D-Link DGS-1250 switch
description:
  - Configures the C(environment temperature threshold thermal) command on a D-Link DGS-1250 switch via SSH.
  - Sets or resets high and low temperature thresholds for environment monitoring.
  - Corresponds to CLI command described in chapter 2-15 of the DGS-1250 CLI Reference Guide.
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
      - Whether to set (C(present)) or reset to default (C(absent)) the thresholds.
    type: str
    choices: [present, absent]
    default: present
  high:
    description:
      - High temperature threshold in Celsius.
      - Range is from -100 to 200.
      - Must be greater than C(low).
    type: int
  low:
    description:
      - Low temperature threshold in Celsius.
      - Range is from -100 to 200.
      - Must be smaller than C(high).
    type: int
notes:
  - Requires C(paramiko) on the Ansible controller (C(pip install paramiko)).
  - The switch must be reachable via SSH from the Ansible controller.
  - This command requires Global Configuration Mode.
  - The low threshold must be smaller than the high threshold.
"""

EXAMPLES = r"""
- name: Set temperature thresholds
  dlink.dgs1250.environment_temperature_threshold:
    host: 192.168.1.1
    username: admin
    password: admin
    high: 100
    low: 20

- name: Reset temperature thresholds to default
  dlink.dgs1250.environment_temperature_threshold:
    host: 192.168.1.1
    username: admin
    password: admin
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

def _build_command(state, high, low):
    """Build the CLI command string."""
    if state == "absent":
        cmd = "no environment temperature threshold thermal"
        if high is not None:
            cmd += " high"
        if low is not None:
            cmd += " low"
        # If neither specified, reset both
        if high is None and low is None:
            cmd += " high low"
        return cmd

    cmd = "environment temperature threshold thermal"
    if high is not None:
        cmd += " high %d" % high
    if low is not None:
        cmd += " low %d" % low
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
            state=dict(type="str", choices=["present", "absent"], default="present"),
            high=dict(type="int"),
            low=dict(type="int"),
        ),
        supports_check_mode=True,
    )

    if not HAS_PARAMIKO:
        module.fail_json(msg="paramiko is required: pip install paramiko")

    state = module.params["state"]
    high = module.params["high"]
    low = module.params["low"]

    if state == "present" and high is None and low is None:
        module.fail_json(msg="At least one of 'high' or 'low' must be specified when state is 'present'.")

    if high is not None and (high < -100 or high > 200):
        module.fail_json(msg="'high' must be between -100 and 200.")

    if low is not None and (low < -100 or low > 200):
        module.fail_json(msg="'low' must be between -100 and 200.")

    if high is not None and low is not None and low >= high:
        module.fail_json(msg="'low' must be smaller than 'high'.")

    host = module.params["host"]
    username = module.params["username"]
    password = module.params["password"]
    port = module.params["port"]
    timeout = module.params["timeout"]

    command = _build_command(state, high, low)
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
