#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dhcpv6_client_show
short_description: Display DHCPv6 settings on a D-Link DGS-1250 switch
description:
  - Executes the C(show ipv6 dhcp) CLI command on a D-Link DGS-1250 switch.
  - Displays DHCPv6 settings, optionally for a specific interface.
  - Corresponds to CLI command described in chapter 18-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface to query (e.g. C(vlan1)). If omitted, general DHCPv6 settings are shown.
    type: str
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display DHCPv6 settings
  jaydee_io.dlink_dgs1250.dhcpv6_client_show:
  register: result

- name: Display DHCPv6 settings for vlan1
  jaydee_io.dlink_dgs1250.dhcpv6_client_show:
    interface: vlan1
  register: result
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
        run_command,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(interface):
    """Build the CLI command string."""
    cmd = "show ipv6 dhcp"
    if interface:
        cmd += " interface %s" % interface
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
        ),
        supports_check_mode=True,
    )

    command = _build_command(module.params["interface"])

    if module.check_mode:
        module.exit_json(changed=False, commands=[command], raw_output="")
        return

    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    module.exit_json(changed=False, raw_output=raw_output, commands=[command])


if __name__ == "__main__":
    main()
