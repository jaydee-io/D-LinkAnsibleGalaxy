#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dns_ip_name_server
short_description: Configure DNS name server on a D-Link DGS-1250 switch
description:
  - Configures the C(ip name-server) CLI command on a D-Link DGS-1250 switch.
  - Adds or removes an IPv4 or IPv6 domain name server address.
  - Corresponds to CLI command described in chapter 23-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  address:
    description:
      - The primary IPv4 or IPv6 address for the domain name server.
      - Required when state is C(present).
    type: str
  address2:
    description:
      - An optional secondary IPv4 or IPv6 address for the domain name server.
    type: str
  state:
    description:
      - C(present) to configure, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Configure DNS server
  jaydee_io.dlink_dgs1250.dns_ip_name_server:
    address: 192.168.5.134
    address2: "5001:5::2"

- name: Remove DNS server
  jaydee_io.dlink_dgs1250.dns_ip_name_server:
    address: 192.168.5.134
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


def _build_commands(address, address2, state):
    """Build the CLI command list."""
    if state == "absent":
        cmd = "no ip name-server %s" % address
        if address2:
            cmd += " %s" % address2
    else:
        cmd = "ip name-server %s" % address
        if address2:
            cmd += " %s" % address2
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            address=dict(type="str"),
            address2=dict(type="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["address"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["address"],
        module.params["address2"],
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
