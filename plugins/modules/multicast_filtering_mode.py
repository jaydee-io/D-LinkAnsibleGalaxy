#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: multicast_filtering_mode
short_description: Configure multicast filtering mode on a D-Link DGS-1250 switch
description:
  - Configures the handling method for multicast packets on a VLAN using the
    C(multicast filtering-mode) CLI command.
  - Use C(state=absent) to revert to the default setting.
  - Corresponds to CLI command described in chapter 28-6 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  vlan_id:
    description:
      - The VLAN ID to configure multicast filtering mode on.
    type: int
    required: true
  mode:
    description:
      - C(forward-all) floods all multicast packets based on the VLAN domain.
      - C(forward-unregistered) forwards registered multicast and floods unregistered.
      - C(filter-unregistered) forwards registered multicast and filters unregistered.
      - Required when C(state=present).
    type: str
    choices: [forward-all, forward-unregistered, filter-unregistered]
  state:
    description:
      - C(present) sets the multicast filtering mode.
      - C(absent) reverts to the default setting.
    type: str
    default: present
    choices: [present, absent]
notes:
  - This command runs in VLAN Configuration Mode.
  - Default mode is C(forward-unregistered).
"""

EXAMPLES = r"""
- name: Set multicast filtering mode to filter-unregistered on VLAN 100
  jaydee_io.dlink_dgs1250.multicast_filtering_mode:
    vlan_id: 100
    mode: filter-unregistered
    state: present

- name: Revert multicast filtering mode to default on VLAN 100
  jaydee_io.dlink_dgs1250.multicast_filtering_mode:
    vlan_id: 100
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


def _build_commands(vlan_id, mode, state):
    if state == "absent":
        return ["vlan %d" % vlan_id, "no multicast filtering-mode", "exit"]
    return ["vlan %d" % vlan_id, "multicast filtering-mode %s" % mode, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_id=dict(type="int", required=True),
            mode=dict(type="str", choices=[
                      "forward-all", "forward-unregistered", "filter-unregistered"]),
            state=dict(type="str", default="present",
                       choices=["present", "absent"]),
        ),
        required_if=[("state", "present", ["mode"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["vlan_id"],
        module.params["mode"],
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
