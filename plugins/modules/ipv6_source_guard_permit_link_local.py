#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_source_guard_permit_link_local
short_description: Enable or disable permit link-local in an IPv6 source guard policy on a D-Link DGS-1250 switch
description:
  - Configures the C(permit link-local) CLI command in Source-guard Policy Configuration Mode on a D-Link DGS-1250 switch.
  - Permits or denies data traffic sent by the link-local address.
  - Corresponds to CLI command described in chapter 38-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.13.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  policy:
    description:
      - Name of the source guard policy to configure.
    type: str
    required: true
  state:
    description:
      - C(enabled) to permit link-local traffic, C(disabled) to deny it.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Source-guard Policy Configuration Mode.
"""

EXAMPLES = r"""
- name: Permit link-local traffic
  jaydee_io.dlink_dgs1250.ipv6_source_guard_permit_link_local:
    policy: policy1

- name: Deny link-local traffic
  jaydee_io.dlink_dgs1250.ipv6_source_guard_permit_link_local:
    policy: policy1
    state: disabled
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


def _build_commands(policy, state):
    """Build the CLI command list."""
    commands = ["ipv6 source-guard policy %s" % policy]
    if state == "enabled":
        commands.append("permit link-local")
    else:
        commands.append("no permit link-local")
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy=dict(type="str", required=True),
            state=dict(type="str", choices=["enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["policy"],
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
