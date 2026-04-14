#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_ipv6_source_guard_policy
short_description: Display IPv6 source guard policy configuration on a D-Link DGS-1250 switch
description:
  - Executes the C(show ipv6 source-guard policy) CLI command on a D-Link DGS-1250 switch.
  - Displays the IPv6 source guard policy configuration.
  - Corresponds to CLI command described in chapter 38-6 of the DGS-1250 CLI Reference Guide.
version_added: "0.13.0"
author:
  - Jérôme Dumesnil
options:
  policy:
    description:
      - Optional policy name. If not specified, all policies are displayed.
    type: str
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display all IPv6 source guard policies
  jaydee_io.dlink_dgs1250.show_ipv6_source_guard_policy:
  register: result

- name: Display a specific IPv6 source guard policy
  jaydee_io.dlink_dgs1250.show_ipv6_source_guard_policy:
    policy: policy1
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


def _build_command(policy):
    if policy:
        return "show ipv6 source-guard policy %s" % policy
    return "show ipv6 source-guard policy"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy=dict(type="str"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["policy"])
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
