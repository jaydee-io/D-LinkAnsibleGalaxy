#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: voice_vlan_enable
short_description: Enable or disable voice VLAN on a D-Link DGS-1250 switch interface
description:
  - Configures the C(voice vlan enable) CLI command on a D-Link DGS-1250 switch interface.
  - Enables or disables the voice VLAN function for a port.
  - Corresponds to CLI command described in chapter 71-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.19.0"
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
  state:
    description:
      - C(enabled) to enable, C(disabled) to disable.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable voice VLAN on port 1
  jaydee_io.dlink_dgs1250.voice_vlan_enable:
    interface: eth1/0/1

- name: Disable voice VLAN on port 1
  jaydee_io.dlink_dgs1250.voice_vlan_enable:
    interface: eth1/0/1
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


def _build_commands(interface, state):
    cmd = "voice vlan enable" if state == "enabled" else "no voice vlan enable"
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
        module.params["interface"], module.params["state"])
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
