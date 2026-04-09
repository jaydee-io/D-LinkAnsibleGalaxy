#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_clear_neighbors
short_description: Clear IPv6 neighbor cache on a D-Link DGS-1250 switch
description:
  - Executes the C(clear ipv6 neighbors) CLI command on a D-Link DGS-1250 switch.
  - Clears IPv6 neighbor cache entries for all interfaces or a specific interface.
  - Corresponds to CLI command described in chapter 10-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.7.0"
author:
  - Jérôme Dumesnil
options:
  target:
    description:
      - Target scope for clearing the IPv6 neighbor cache.
      - C(all) clears all entries.
      - C(interface) clears entries for a specific interface.
    type: str
    required: true
    choices: [all, interface]
  value:
    description:
      - Interface ID (when C(target=interface)).
      - Required when C(target) is C(interface).
    type: str
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear all IPv6 neighbor cache entries
  jaydee_io.dlink_dgs1250.ipv6_clear_neighbors:
    target: all

- name: Clear IPv6 neighbor cache for an interface
  jaydee_io.dlink_dgs1250.ipv6_clear_neighbors:
    target: interface
    value: vlan1
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


def _build_commands(target, value):
    """Build the CLI command list."""
    if target == "all":
        return ["clear ipv6 neighbors all"]
    # target == "interface"
    return ["clear ipv6 neighbors interface %s" % value]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            target=dict(type="str", required=True, choices=["all", "interface"]),
            value=dict(type="str"),
        ),
        required_if=[
            ("target", "interface", ["value"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["target"],
        module.params["value"],
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
