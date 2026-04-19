#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: impb_clear_violation
short_description: Clear IMPB violation entries on a D-Link DGS-1250 switch
description:
  - Executes the C(clear ip ip-mac-port-binding violation) CLI command on a D-Link DGS-1250 switch.
  - Clears IMPB blocked entries for all, a specific interface, or a specific MAC address.
  - Corresponds to CLI command described in chapter 32-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.12.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  target:
    description:
      - C(all) clears all violation entries.
      - C(interface) clears entries for a specific interface (requires C(interface_id)).
      - C(mac_address) clears entries for a specific MAC address (requires C(mac_addr)).
    type: str
    required: true
    choices: [all, interface, mac_address]
  interface_id:
    description:
      - The interface ID (e.g. C(eth1/0/4)). Required when C(target=interface).
    type: str
  mac_addr:
    description:
      - The MAC address to clear. Required when C(target=mac_address).
    type: str
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear all IMPB violation entries
  jaydee_io.dlink_dgs1250.impb_clear_violation:
    target: all

- name: Clear IMPB violation entries for interface
  jaydee_io.dlink_dgs1250.impb_clear_violation:
    target: interface
    interface_id: eth1/0/4

- name: Clear IMPB violation entries for MAC address
  jaydee_io.dlink_dgs1250.impb_clear_violation:
    target: mac_address
    mac_addr: "01-00-0C-CC-CC-CC"
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


def _build_commands(target, interface_id, mac_addr):
    if target == "all":
        return ["clear ip ip-mac-port-binding violation all"]
    elif target == "interface":
        return ["clear ip ip-mac-port-binding violation interface %s" % interface_id]
    else:
        return ["clear ip ip-mac-port-binding violation %s" % mac_addr]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            target=dict(type="str", required=True, choices=["all", "interface", "mac_address"]),
            interface_id=dict(type="str"),
            mac_addr=dict(type="str"),
        ),
        required_if=[
            ("target", "interface", ["interface_id"]),
            ("target", "mac_address", ["mac_addr"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["target"],
        module.params["interface_id"],
        module.params["mac_addr"],
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
