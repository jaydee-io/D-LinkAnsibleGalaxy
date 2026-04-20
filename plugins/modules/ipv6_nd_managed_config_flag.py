#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_nd_managed_config_flag
short_description: Configure IPv6 ND managed-config-flag on an interface of a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 nd managed-config-flag) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables the managed address configuration flag in IPv6 router advertisements.
  - Corresponds to CLI command described in chapter 10-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.7.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface on which to configure the managed-config-flag (e.g. C(vlan1)).
    type: str
    required: true
  state:
    description:
      - Whether to enable (C(enabled)) or disable (C(disabled)) the managed-config-flag.
    type: str
    choices: [enabled, disabled]
    default: enabled
"""

EXAMPLES = r"""
- name: Enable managed-config-flag on vlan1
  jaydee_io.dlink_dgs1250.ipv6_nd_managed_config_flag:
    interface: vlan1

- name: Disable managed-config-flag on vlan1
  jaydee_io.dlink_dgs1250.ipv6_nd_managed_config_flag:
    interface: vlan1
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


def _build_commands(interface, state):
    """Build the CLI command list."""
    if state == "enabled":
        cmd = "ipv6 nd managed-config-flag"
    else:
        cmd = "no ipv6 nd managed-config-flag"
    return ["interface %s" % interface, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            state=dict(type="str", choices=[
                       "enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"],
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
