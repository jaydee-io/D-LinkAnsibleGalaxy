#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: network_protocol_port_protect
short_description: Enable or disable network protocol port protection on a D-Link DGS-1250 switch
description:
  - Configures the C(network-protocol-port protect) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables TCP or UDP port protection.
  - Corresponds to CLI command described in chapter 49-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.15.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  protocol:
    description:
      - The protocol to protect.
    type: str
    required: true
    choices: [tcp, udp]
  state:
    description:
      - C(enabled) to enable port protection, C(disabled) to disable it.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable TCP port protection
  jaydee_io.dlink_dgs1250.network_protocol_port_protect:
    protocol: tcp

- name: Disable UDP port protection
  jaydee_io.dlink_dgs1250.network_protocol_port_protect:
    protocol: udp
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
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(protocol, state):
    """Build the CLI command list."""
    if state == "enabled":
        return ["network-protocol-port protect %s" % protocol]
    return ["no network-protocol-port protect %s" % protocol]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            protocol=dict(type="str", required=True, choices=["tcp", "udp"]),
            state=dict(type="str", choices=["enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["protocol"],
        module.params["state"],
    )
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
