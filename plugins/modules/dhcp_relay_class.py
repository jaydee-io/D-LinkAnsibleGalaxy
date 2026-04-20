#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_relay_class
short_description: Associate a DHCP class with a relay pool on a D-Link DGS-1250 switch
description:
  - Configures the C(class) CLI command in DHCP Pool Configuration Mode on a D-Link DGS-1250 switch.
  - Associates or removes a DHCP class from a DHCP relay pool.
  - Corresponds to CLI command described in chapter 16-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  pool:
    description:
      - Name of the DHCP relay pool to configure.
    type: str
    required: true
  name:
    description:
      - Name of the DHCP class to associate with the pool.
    type: str
    required: true
  state:
    description:
      - C(present) to associate the class, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in DHCP Pool Configuration Mode.
"""

EXAMPLES = r"""
- name: Associate DHCP class with pool
  jaydee_io.dlink_dgs1250.dhcp_relay_class:
    pool: POOL1
    name: CLASS1

- name: Remove DHCP class from pool
  jaydee_io.dlink_dgs1250.dhcp_relay_class:
    pool: POOL1
    name: CLASS1
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


def _build_commands(pool, name, state):
    """Build the CLI command list."""
    commands = ["ip dhcp pool %s" % pool]
    if state == "absent":
        commands.append("no class %s" % name)
    else:
        commands.append("class %s" % name)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            pool=dict(type="str", required=True),
            name=dict(type="str", required=True),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["pool"],
        module.params["name"],
        module.params["state"],
    )

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
