#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ip_ssh_service_port
short_description: Configure the SSH service port on a D-Link DGS-1250 switch
description:
  - Configures the C(ip ssh service-port) CLI command on a D-Link DGS-1250 switch.
  - Specifies the TCP port for the SSH server.
  - Corresponds to CLI command described in chapter 58-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  port:
    description:
      - TCP port number (1-65535). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the port, C(absent) to revert to default (22).
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set SSH port to 3000
  jaydee_io.dlink_dgs1250.ip_ssh_service_port:
    port: 3000

- name: Revert to default port
  jaydee_io.dlink_dgs1250.ip_ssh_service_port:
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


def _build_commands(port, state):
    if state == "absent":
        return ["no ip ssh service-port"]
    return ["ip ssh service-port %d" % port]



def main():
    module = AnsibleModule(
        argument_spec=dict(
            port=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["port"])],
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["port"], module.params["state"])
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
