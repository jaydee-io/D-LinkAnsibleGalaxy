#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: auth_clear_sessions
short_description: Clear authentication sessions on a D-Link DGS-1250 switch
description:
  - Executes the C(clear authentication sessions) CLI command on a D-Link DGS-1250 switch.
  - Clears authentication sessions by type, interface, or MAC address.
  - Corresponds to CLI command described in chapter 48-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.15.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  target:
    description:
      - C(dot1x) clears all 802.1X sessions.
      - C(all) clears all sessions.
      - C(interface) clears sessions on a specific port (requires C(interface_id)).
      - C(mac_address) clears a specific user session (requires C(mac_address)).
    type: str
    required: true
    choices: [dot1x, all, interface, mac_address]
  interface_id:
    description:
      - The interface ID (e.g. C(eth1/0/1)). Required when C(target=interface).
    type: str
  mac_address:
    description:
      - The MAC address to clear (e.g. C(00-E0-4C-68-2D-6F)). Required when C(target=mac_address).
    type: str
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear all authentication sessions
  jaydee_io.dlink_dgs1250.auth_clear_sessions:
    target: all

- name: Clear 802.1X authentication sessions
  jaydee_io.dlink_dgs1250.auth_clear_sessions:
    target: dot1x

- name: Clear authentication sessions on port 1
  jaydee_io.dlink_dgs1250.auth_clear_sessions:
    target: interface
    interface_id: eth1/0/1

- name: Clear authentication session by MAC address
  jaydee_io.dlink_dgs1250.auth_clear_sessions:
    target: mac_address
    mac_address: 00-E0-4C-68-2D-6F
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
        run_commands, MODE_PRIVILEGED,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


def _build_commands(target, interface_id, mac_address):
    if target == "dot1x":
        return ["clear authentication sessions dot1x"]
    elif target == "all":
        return ["clear authentication sessions all"]
    elif target == "interface":
        return ["clear authentication sessions interface %s" % interface_id]
    else:
        return ["clear authentication sessions mac-address %s" % mac_address]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            target=dict(type="str", required=True, choices=["dot1x", "all", "interface", "mac_address"]),
            interface_id=dict(type="str"),
            mac_address=dict(type="str"),
        ),
        required_if=[
            ("target", "interface", ["interface_id"]),
            ("target", "mac_address", ["mac_address"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["target"],
        module.params["interface_id"],
        module.params["mac_address"],
    )
    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_PRIVILEGED)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
