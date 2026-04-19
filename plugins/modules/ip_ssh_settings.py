#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ip_ssh_settings
short_description: Configure SSH timeout and authentication retries on a D-Link DGS-1250 switch
description:
  - Configures the C(ip ssh timeout) and C(ip ssh authentication-retries) CLI commands on a D-Link DGS-1250 switch.
  - Sets the SSH negotiation timeout and/or authentication retry count.
  - Corresponds to CLI command described in chapter 58-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  timeout:
    description:
      - SSH negotiation timeout in seconds (30-600).
    type: int
  authentication_retries:
    description:
      - Number of authentication retry attempts (1-32).
    type: int
  state:
    description:
      - C(present) to set values, C(absent) to revert to defaults.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set SSH timeout
  jaydee_io.dlink_dgs1250.ip_ssh_settings:
    timeout: 160

- name: Set SSH authentication retries
  jaydee_io.dlink_dgs1250.ip_ssh_settings:
    authentication_retries: 2

- name: Revert both to defaults
  jaydee_io.dlink_dgs1250.ip_ssh_settings:
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


def _build_commands(timeout, authentication_retries, state):
    commands = []
    if state == "absent":
        commands.append("no ip ssh timeout")
        commands.append("no ip ssh authentication-retries")
    else:
        if timeout is not None:
            commands.append("ip ssh timeout %d" % timeout)
        if authentication_retries is not None:
            commands.append("ip ssh authentication-retries %d" %
                            authentication_retries)
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            timeout=dict(type="int"),
            authentication_retries=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["timeout"], module.params["authentication_retries"], module.params["state"])
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
