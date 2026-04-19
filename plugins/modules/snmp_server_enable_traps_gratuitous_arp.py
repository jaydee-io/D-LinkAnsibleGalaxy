#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: snmp_server_enable_traps_gratuitous_arp
short_description: Enable SNMP notifications for gratuitous ARP on a D-Link DGS-1250 switch
description:
  - Enables or disables SNMP notifications for gratuitous ARP duplicate IP detection using the
    C(snmp-server enable traps gratuitous-arp) CLI command.
  - Corresponds to CLI command described in chapter 29-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  state:
    description:
      - C(present) enables SNMP notifications for gratuitous ARP.
      - C(absent) disables SNMP notifications for gratuitous ARP.
    type: str
    default: present
    choices: [present, absent]
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable SNMP notifications for gratuitous ARP
  jaydee_io.dlink_dgs1250.snmp_server_enable_traps_gratuitous_arp:
    state: present

- name: Disable SNMP notifications for gratuitous ARP
  jaydee_io.dlink_dgs1250.snmp_server_enable_traps_gratuitous_arp:
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


def _build_commands(state):
    if state == "absent":
        return ["no snmp-server enable traps gratuitous-arp"]
    return ["snmp-server enable traps gratuitous-arp"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", default="present", choices=["present", "absent"]),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["state"])
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
