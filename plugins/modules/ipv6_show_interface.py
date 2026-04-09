#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_show_interface
short_description: Display IPv6 interface information on a D-Link DGS-1250 switch
description:
  - Executes the C(show ipv6 interface) CLI command on a D-Link DGS-1250 switch.
  - Returns IPv6 interface configuration and status information.
  - Corresponds to CLI command described in chapter 10-16 of the DGS-1250 CLI Reference Guide.
version_added: "0.7.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - Interface to query (e.g. C(vlan1)). If omitted, all interfaces are shown.
    type: str
  brief:
    description:
      - When C(true), show brief output format.
    type: bool
    default: false
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
"""

EXAMPLES = r"""
- name: Show all IPv6 interfaces
  jaydee_io.dlink_dgs1250.ipv6_show_interface:
  register: result

- name: Show IPv6 interface for vlan1 (brief)
  jaydee_io.dlink_dgs1250.ipv6_show_interface:
    interface: vlan1
    brief: true
  register: result
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import run_command
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(interface, brief):
    """Build the CLI command string."""
    cmd = "show ipv6 interface"
    if interface:
        cmd += " %s" % interface
    if brief:
        cmd += " brief"
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
            brief=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )

    cmd = _build_command(
        module.params["interface"],
        module.params["brief"],
    )

    try:
        raw_output = run_command(module, cmd)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    module.exit_json(changed=False, raw_output=raw_output)


if __name__ == "__main__":
    main()
