#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ipv4_clear_arp_cache
short_description: Clear ARP cache on a D-Link DGS-1250 switch
description:
  - Executes the C(clear arp-cache) CLI command on a D-Link DGS-1250 switch.
  - Clears ARP cache entries for all interfaces, a specific interface, or a specific IP address.
  - Corresponds to CLI command described in chapter 9-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  target:
    description:
      - Target scope for clearing the ARP cache.
      - C(all) clears all entries.
      - C(interface) clears entries for a specific interface.
      - C(ip) clears the entry for a specific IP address.
    type: str
    required: true
    choices: [all, interface, ip]
  value:
    description:
      - Interface ID (when C(target=interface)) or IP address (when C(target=ip)).
      - Required when C(target) is C(interface) or C(ip).
    type: str
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear all ARP cache entries
  jaydee_io.dlink_dgs1250.ipv4_clear_arp_cache:
    target: all

- name: Clear ARP cache for an interface
  jaydee_io.dlink_dgs1250.ipv4_clear_arp_cache:
    target: interface
    value: vlan1

- name: Clear ARP cache for a specific IP
  jaydee_io.dlink_dgs1250.ipv4_clear_arp_cache:
    target: ip
    value: 10.0.0.1
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


def _build_commands(target, value):
    """Build the CLI command list."""
    if target == "all":
        return ["clear arp-cache all"]
    if target == "interface":
        return ["clear arp-cache interface %s" % value]
    # target == "ip"
    return ["clear arp-cache %s" % value]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            target=dict(type="str", required=True, choices=[
                        "all", "interface", "ip"]),
            value=dict(type="str"),
        ),
        required_if=[
            ("target", "interface", ["value"]),
            ("target", "ip", ["value"]),
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
