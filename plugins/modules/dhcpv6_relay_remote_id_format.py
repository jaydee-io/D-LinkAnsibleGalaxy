#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dhcpv6_relay_remote_id_format
short_description: Configure DHCPv6 relay remote-id format on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 dhcp relay remote-id format) CLI command on a D-Link DGS-1250 switch.
  - Sets or removes the sub-type of the remote ID.
  - Corresponds to CLI command described in chapter 20-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  format:
    description:
      - The remote-id format to set. Required when C(state=present).
    type: str
    choices: [cid-with-user-define, default, expert-udf, user-define]
  state:
    description:
      - C(present) to set, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set DHCPv6 relay remote-id format to cid-with-user-define
  jaydee_io.dlink_dgs1250.dhcpv6_relay_remote_id_format:
    format: cid-with-user-define

- name: Reset DHCPv6 relay remote-id format to default
  jaydee_io.dlink_dgs1250.dhcpv6_relay_remote_id_format:
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


def _build_commands(fmt, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no ipv6 dhcp relay remote-id format"]
    return ["ipv6 dhcp relay remote-id format %s" % fmt]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            format=dict(type="str", choices=["cid-with-user-define", "default", "expert-udf", "user-define"]),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["format"])],
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["format"], module.params["state"])

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
