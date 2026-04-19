#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mgmt_session_timeout
short_description: Set session timeout on a D-Link DGS-1250 switch
description:
  - Configures the C(session-timeout) CLI command on a D-Link DGS-1250 switch.
  - Sets the idle timeout in minutes for a line (console, telnet, ssh).
  - Corresponds to CLI command described in chapter 5-20 of the DGS-1250 CLI Reference Guide.
version_added: "0.4.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  line:
    description:
      - Line type to configure.
    type: str
    required: true
    choices: [console, telnet, ssh]
  timeout:
    description:
      - Session timeout in minutes. Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the timeout, C(absent) to reset to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command requires Line Configuration Mode.
"""

EXAMPLES = r"""
- name: Set Telnet session timeout to 30 minutes
  jaydee_io.dlink_dgs1250.mgmt_session_timeout:
    line: telnet
    timeout: 30

- name: Reset SSH session timeout to default
  jaydee_io.dlink_dgs1250.mgmt_session_timeout:
    line: ssh
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


def _build_commands(line, timeout, state):
    cmds = ["line %s" % line]
    if state == "absent":
        cmds.append("no session-timeout")
    else:
        cmds.append("session-timeout %d" % timeout)
    cmds.append("exit")
    return cmds


def main():
    module = AnsibleModule(
        argument_spec=dict(
            line=dict(type="str", required=True, choices=[
                      "console", "telnet", "ssh"]),
            timeout=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["timeout"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["line"], module.params["timeout"], module.params["state"])

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
