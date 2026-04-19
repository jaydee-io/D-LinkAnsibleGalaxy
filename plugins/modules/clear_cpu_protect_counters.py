#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: clear_cpu_protect_counters
short_description: Clear CPU protect counters on a D-Link DGS-1250 switch
description:
  - Executes the C(clear cpu-protect counters) CLI command on a D-Link DGS-1250 switch.
  - Clears CPU protect related counters.
  - Corresponds to CLI command described in chapter 57-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  target:
    description:
      - What to clear. C(all) clears all counters. C(sub-interface) clears sub-interface counters.
        C(type) clears protocol counters.
    type: str
    required: true
    choices: [all, sub-interface, type]
  sub_interface:
    description:
      - Sub-interface to clear (C(manage), C(protocol), C(route)).
        If omitted when C(target=sub-interface), all sub-interfaces are cleared.
    type: str
    choices: [manage, protocol, route]
  protocol_name:
    description:
      - Protocol name to clear. If omitted when C(target=type), all protocols are cleared.
    type: str
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear all CPU protect counters
  jaydee_io.dlink_dgs1250.clear_cpu_protect_counters:
    target: all

- name: Clear manage sub-interface counters
  jaydee_io.dlink_dgs1250.clear_cpu_protect_counters:
    target: sub-interface
    sub_interface: manage

- name: Clear ARP protocol counters
  jaydee_io.dlink_dgs1250.clear_cpu_protect_counters:
    target: type
    protocol_name: arp
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
        run_commands, MODE_PRIVILEGED,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


def _build_commands(target, sub_interface, protocol_name):
    if target == "all":
        return ["clear cpu-protect counters all"]
    elif target == "sub-interface":
        cmd = "clear cpu-protect counters sub-interface"
        if sub_interface:
            cmd += " %s" % sub_interface
        return [cmd]
    else:
        cmd = "clear cpu-protect counters type"
        if protocol_name:
            cmd += " %s" % protocol_name
        return [cmd]



def main():
    module = AnsibleModule(
        argument_spec=dict(
            target=dict(type="str", required=True, choices=["all", "sub-interface", "type"]),
            sub_interface=dict(type="str", choices=["manage", "protocol", "route"]),
            protocol_name=dict(type="str"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["target"], module.params["sub_interface"], module.params["protocol_name"])
    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_PRIVILEGED)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
