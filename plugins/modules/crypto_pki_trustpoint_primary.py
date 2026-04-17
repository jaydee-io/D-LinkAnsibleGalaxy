#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: crypto_pki_trustpoint_primary
short_description: Set a trust point as primary on a D-Link DGS-1250 switch
description:
  - Configures the C(primary) CLI command inside CA-Trust-Point Configuration Mode on a D-Link DGS-1250 switch.
  - Assigns or removes a trust-point as the primary trust-point.
  - Corresponds to CLI command described in chapter 59-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil
options:
  trustpoint:
    description:
      - The trust-point name.
    type: str
    required: true
  state:
    description:
      - C(present) to set as primary, C(absent) to unbind.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in CA-Trust-Point Configuration Mode.
"""

EXAMPLES = r"""
- name: Set TP1 as primary
  jaydee_io.dlink_dgs1250.crypto_pki_trustpoint_primary:
    trustpoint: TP1

- name: Remove primary designation
  jaydee_io.dlink_dgs1250.crypto_pki_trustpoint_primary:
    trustpoint: TP1
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


def _build_commands(trustpoint, state):
    commands = ["crypto pki trustpoint %s" % trustpoint]
    if state == "absent":
        commands.append("no primary")
    else:
        commands.append("primary")
    commands.append("exit")
    return commands



def main():
    module = AnsibleModule(
        argument_spec=dict(
            trustpoint=dict(type="str", required=True),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["trustpoint"], module.params["state"])
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
