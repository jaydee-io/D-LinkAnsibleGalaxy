#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_snooping_limit_entries
short_description: Configure DHCP snooping entry limit on an interface on a D-Link DGS-1250 switch
description:
  - Configures the C(ip dhcp snooping limit entries) CLI command on a D-Link DGS-1250 switch.
  - Corresponds to CLI command described in chapter 17-9 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  entries:
    description:
      - The number of DHCP snooping binding entries (0-1024). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set limit, C(absent) to reset.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set entry limit to 100 on port 1
  jaydee_io.dlink_dgs1250.dhcp_snooping_limit_entries:
    interface: eth1/0/1
    entries: 100
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


def _build_commands(interface, entries, state):
    """Build the CLI command list."""
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no ip dhcp snooping limit entries")
    else:
        commands.append("ip dhcp snooping limit entries %s" % entries)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            entries=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["entries"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"], module.params["entries"], module.params["state"])
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
