#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dns_ip_host
short_description: Configure static host name to IP address mapping on a D-Link DGS-1250 switch
description:
  - Configures the C(ip host) CLI command on a D-Link DGS-1250 switch.
  - Adds or removes a static mapping entry for a host name and IP address.
  - Corresponds to CLI command described in chapter 23-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  host_name:
    description:
      - The host name of the equipment. Must be a fully qualified host name.
    type: str
    required: true
  address:
    description:
      - The IPv4 or IPv6 address of the equipment.
      - Required when state is C(present).
    type: str
  state:
    description:
      - C(present) to add, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Add static host entry
  jaydee_io.dlink_dgs1250.dns_ip_host:
    host_name: www.abc.com
    address: 192.168.5.243

- name: Remove static host entry
  jaydee_io.dlink_dgs1250.dns_ip_host:
    host_name: www.abc.com
    address: 192.168.5.243
    state: absent
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


def _build_commands(host_name, address, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no ip host %s %s" % (host_name, address)]
    else:
        return ["ip host %s %s" % (host_name, address)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            host_name=dict(type="str", required=True),
            address=dict(type="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["address"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["host_name"],
        module.params["address"],
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
