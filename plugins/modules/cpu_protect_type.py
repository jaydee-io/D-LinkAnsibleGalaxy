#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: cpu_protect_type
short_description: Configure CPU protect rate limit by protocol type on a D-Link DGS-1250 switch
description:
  - Configures the C(cpu-protect type) CLI command on a D-Link DGS-1250 switch.
  - Sets the rate limit of traffic destined for the CPU by protocol type.
  - Corresponds to CLI command described in chapter 57-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  protocol_name:
    description:
      - The protocol name to configure.
    type: str
    required: true
  rate:
    description:
      - Threshold value in packets per second. 0 drops all packets. Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the rate limit, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Limit ARP to 100 pps
  jaydee_io.dlink_dgs1250.cpu_protect_type:
    protocol_name: arp
    rate: 100

- name: Revert ARP rate limit
  jaydee_io.dlink_dgs1250.cpu_protect_type:
    protocol_name: arp
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(protocol_name, rate, state):
    if state == "absent":
        return ["no cpu-protect type %s" % protocol_name]
    return ["cpu-protect type %s pps %d" % (protocol_name, rate)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            protocol_name=dict(type="str", required=True),
            rate=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["rate"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["protocol_name"], module.params["rate"], module.params["state"])
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
