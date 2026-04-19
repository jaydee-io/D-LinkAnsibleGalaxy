#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: acl_hardware_counter
short_description: Enable or disable ACL hardware counter on a D-Link DGS-1250 switch
description:
  - Configures the C(acl-hardware-counter access-group) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables hardware packet counting for a specified ACL.
  - Corresponds to CLI command described in chapter 4-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.3.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  name:
    description:
      - Name or number of the access list.
    type: str
    required: true
  state:
    description:
      - C(enabled) to enable the hardware counter, C(disabled) to disable it.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command requires Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable ACL hardware counter for access-list 'abc'
  jaydee_io.dlink_dgs1250.acl_hardware_counter:
    name: abc

- name: Disable ACL hardware counter for access-list 'abc'
  jaydee_io.dlink_dgs1250.acl_hardware_counter:
    name: abc
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
        run_commands, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(name, state):
    prefix = "" if state == "enabled" else "no "
    return ["%sacl-hardware-counter access-group %s" % (prefix, name)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            state=dict(type="str", choices=[
                       "enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["name"], module.params["state"])

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
