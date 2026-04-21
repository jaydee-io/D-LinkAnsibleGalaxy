#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dot1x_forward_pdu
short_description: Enable or disable 802.1X PDU forwarding on a D-Link DGS-1250 switch port
description:
  - Configures the C(dot1x forward-pdu) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables the forwarding of 802.1X PDU on a specific port.
  - Corresponds to CLI command described in chapter 3-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.2.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Physical port interface to configure (e.g. C(eth1/0/1)).
    required: true
    type: str
  state:
    description:
      - Whether to enable (C(enabled)) or disable (C(disabled)) PDU forwarding.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Interface Configuration Mode.
  - PDU forwarding only takes effect when 802.1X authentication is disabled on the port.
"""

EXAMPLES = r"""
- name: Enable PDU forwarding on port 1
  jaydee_io.dlink_dgs1250.dot1x_forward_pdu:
    interface: eth1/0/1

- name: Disable PDU forwarding on port 1
  jaydee_io.dlink_dgs1250.dot1x_forward_pdu:
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
        run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(interface, state):
    """Build the CLI command list for interface configuration."""
    commands = ["interface %s" % interface]
    if state == "enabled":
        commands.append("dot1x forward-pdu")
    else:
        commands.append("no dot1x forward-pdu")
    return commands


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            state=dict(type="str", choices=[
                       "enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )

    interface = module.params["interface"]
    state = module.params["state"]

    commands = _build_commands(interface, state)

    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
    diff = build_config_diff(module, commands) if module._diff else None
    if module.check_mode:
        result = dict(changed=True, commands=commands, raw_output="")
        if diff:
            result['diff'] = diff
        module.exit_json(**result)
        return

    try:
        raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    result = dict(changed=True, raw_output=raw_output, commands=commands)
    if diff:
        result['diff'] = diff
    module.exit_json(**result)


if __name__ == "__main__":
    main()
