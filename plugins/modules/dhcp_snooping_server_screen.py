#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_snooping_server_screen
short_description: Configure DHCP snooping server screening on an interface on a D-Link DGS-1250 switch
description:
  - Configures the C(ip dhcp snooping server-screen) CLI command on a D-Link DGS-1250 switch.
  - Corresponds to CLI command described in chapter 17-20 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure.
    type: str
    required: true
  server_ip:
    description:
      - The trusted DHCP server IP address.
    type: str
  profile:
    description:
      - The server screen profile name.
    type: str
  state:
    description:
      - C(present) to enable, C(absent) to disable server screening.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable server screening with IP and profile
  jaydee_io.dlink_dgs1250.dhcp_snooping_server_screen:
    interface: eth1/0/3
    server_ip: 10.1.1.2
    profile: campus-profile
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


def _build_commands(interface, server_ip, profile, state):
    """Build the CLI command list."""
    commands = ["interface %s" % interface]
    if state == "absent":
        cmd = "no ip dhcp snooping server-screen"
        if server_ip:
            cmd += " %s" % server_ip
        commands.append(cmd)
    else:
        cmd = "ip dhcp snooping server-screen"
        if server_ip:
            cmd += " %s" % server_ip
            if profile:
                cmd += " profile %s" % profile
        commands.append(cmd)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            server_ip=dict(type="str"),
            profile=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"], module.params["server_ip"], module.params["profile"], module.params["state"])
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
