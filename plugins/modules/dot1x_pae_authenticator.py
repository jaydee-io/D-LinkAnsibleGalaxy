#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dot1x_pae_authenticator
short_description: Enable or disable 802.1X PAE authenticator on a D-Link DGS-1250 switch port
description:
  - Configures the C(dot1x pae authenticator) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables a port as an IEEE 802.1X port access entity (PAE) authenticator.
  - Corresponds to CLI command described in chapter 3-8 of the DGS-1250 CLI Reference Guide.
version_added: "0.2.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - Physical port interface to configure (e.g. C(eth1/0/1)).
    required: true
    type: str
  state:
    description:
      - Whether to enable (C(enabled)) or disable (C(disabled)) the PAE authenticator.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Interface Configuration Mode.
  - 802.1X must be globally enabled with C(dot1x system-auth-control) for this to take effect.
"""

EXAMPLES = r"""
- name: Enable PAE authenticator on port 1
  jaydee_io.dlink_dgs1250.dot1x_pae_authenticator:
    interface: eth1/0/1

- name: Disable PAE authenticator on port 1
  jaydee_io.dlink_dgs1250.dot1x_pae_authenticator:
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
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(interface, state):
    """Build the CLI command list for interface configuration."""
    commands = ["interface %s" % interface]
    if state == "enabled":
        commands.append("dot1x pae authenticator")
    else:
        commands.append("no dot1x pae authenticator")
    return commands


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            state=dict(type="str", choices=["enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )

    interface = module.params["interface"]
    state = module.params["state"]

    commands = _build_commands(interface, state)

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
