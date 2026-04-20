#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: impb_enable
short_description: Enable or disable IMPB access control on an interface on a D-Link DGS-1250 switch
description:
  - Configures the C(ip ip-mac-port-binding) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables IP-MAC-Port Binding access control on an interface.
  - Corresponds to CLI command described in chapter 32-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.12.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/10)).
    type: str
    required: true
  mode:
    description:
      - The IMPB access control mode. Only used when C(state=enabled).
      - C(strict-mode) performs strict mode access control.
      - C(loose-mode) performs loose mode access control.
      - If not specified when enabling, defaults to C(strict-mode).
    type: str
    choices: [strict-mode, loose-mode]
  state:
    description:
      - Whether to enable (C(enabled)) or disable (C(disabled)) IMPB.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable IMPB in strict mode on interface
  jaydee_io.dlink_dgs1250.impb_enable:
    interface: eth1/0/10
    mode: strict-mode

- name: Enable IMPB in loose mode on interface
  jaydee_io.dlink_dgs1250.impb_enable:
    interface: eth1/0/10
    mode: loose-mode

- name: Disable IMPB on interface
  jaydee_io.dlink_dgs1250.impb_enable:
    interface: eth1/0/10
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


def _build_commands(interface, mode, state):
    commands = ["interface %s" % interface]
    if state == "disabled":
        commands.append("no ip ip-mac-port-binding")
    elif mode:
        commands.append("ip ip-mac-port-binding %s" % mode)
    else:
        commands.append("ip ip-mac-port-binding")
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            mode=dict(type="str", choices=["strict-mode", "loose-mode"]),
            state=dict(type="str", choices=[
                       "enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["mode"],
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
