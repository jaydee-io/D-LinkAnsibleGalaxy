#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dhcpv6_guard_show_policy
short_description: Display DHCPv6 guard policy information on a D-Link DGS-1250 switch
description:
  - Executes the C(show ipv6 dhcp guard policy) CLI command on a D-Link DGS-1250 switch.
  - Displays DHCPv6 guard policy information, optionally for a specific policy.
  - Corresponds to CLI command described in chapter 19-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  policy_name:
    description:
      - Name of the DHCPv6 guard policy to display. If omitted, all policies are shown.
    type: str
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display all DHCPv6 guard policies
  jaydee_io.dlink_dgs1250.dhcpv6_guard_show_policy:
  register: result

- name: Display a specific DHCPv6 guard policy
  jaydee_io.dlink_dgs1250.dhcpv6_guard_show_policy:
    policy_name: POLICY1
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(policy_name):
    """Build the CLI command string."""
    cmd = "show ipv6 dhcp guard policy"
    if policy_name:
        cmd += " %s" % policy_name
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_name=dict(type="str"),
        ),
        supports_check_mode=True,
    )

    command = _build_command(module.params["policy_name"])

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
