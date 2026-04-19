#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dhcpv6_client_clear
short_description: Restart DHCPv6 client on an interface of a D-Link DGS-1250 switch
description:
  - Executes the C(clear ipv6 dhcp client) CLI command on a D-Link DGS-1250 switch.
  - Restarts the DHCPv6 client process on the specified VLAN interface.
  - Corresponds to CLI command described in chapter 18-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface_id:
    description:
      - VLAN interface on which to restart the DHCPv6 client (e.g. C(vlan1)).
    type: str
    required: true
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Restart DHCPv6 client on vlan1
  jaydee_io.dlink_dgs1250.dhcpv6_client_clear:
    interface_id: vlan1

- name: Restart DHCPv6 client on vlan 100
  jaydee_io.dlink_dgs1250.dhcpv6_client_clear:
    interface_id: vlan 100
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


def _build_commands(interface_id):
    """Build the CLI command list."""
    return ["clear ipv6 dhcp client %s" % interface_id]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface_id=dict(type="str", required=True),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["interface_id"])

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
