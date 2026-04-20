#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_source_guard_attach_policy
short_description: Attach an IPv6 source guard policy to an interface on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 source-guard attach-policy) CLI command in Interface Configuration Mode on a D-Link DGS-1250 switch.
  - Applies an IPv6 source guard policy on an interface.
  - Corresponds to CLI command described in chapter 38-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.13.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/3)).
    type: str
    required: true
  policy:
    description:
      - Name of the source guard policy. Optional; if not specified with C(state=present), the default policy is used.
    type: str
  state:
    description:
      - C(present) to attach the policy, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Attach source guard policy to interface
  jaydee_io.dlink_dgs1250.ipv6_source_guard_attach_policy:
    interface: eth1/0/3
    policy: pol1

- name: Attach default source guard policy to interface
  jaydee_io.dlink_dgs1250.ipv6_source_guard_attach_policy:
    interface: eth1/0/3

- name: Remove source guard policy from interface
  jaydee_io.dlink_dgs1250.ipv6_source_guard_attach_policy:
    interface: eth1/0/3
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
        run_commands, is_config_present, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, MODE_GLOBAL_CONFIG


def _build_commands(interface, policy, state):
    """Build the CLI command list."""
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no ipv6 source-guard attach-policy")
    elif policy:
        commands.append("ipv6 source-guard attach-policy %s" % policy)
    else:
        commands.append("ipv6 source-guard attach-policy")
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            policy=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["policy"],
        module.params["state"],
    )
    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
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
