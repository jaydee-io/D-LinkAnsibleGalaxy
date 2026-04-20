#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mld_snooping_mrouter
short_description: Configure MLD snooping multicast router ports on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 mld snooping mrouter) CLI command on a D-Link DGS-1250 switch.
  - Adds or removes static/forbidden multicast router ports or configures dynamic learning on a VLAN.
  - Corresponds to CLI command described in chapter 45-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - "Jérôme Dumesnil (@jaydee-io)"
options:
  vlan_id:
    description:
      - The VLAN ID to configure.
    type: int
    required: true
  type:
    description:
      - C(interface) configures a static multicast router port.
      - C(forbidden) configures a forbidden multicast router port.
      - C(learn-pimv6) configures dynamic learning of routing protocol packets.
    type: str
    required: true
    choices: [interface, forbidden, learn-pimv6]
  interface_id:
    description:
      - The interface ID (e.g. C(eth1/0/1)). Required when C(type=interface) or C(type=forbidden).
    type: str
  state:
    description:
      - C(present) to add, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in VLAN Configuration Mode.
"""

EXAMPLES = r"""
- name: Add static multicast router port on VLAN 1
  jaydee_io.dlink_dgs1250.mld_snooping_mrouter:
    vlan_id: 1
    type: interface
    interface_id: eth1/0/1

- name: Add forbidden multicast router port on VLAN 1
  jaydee_io.dlink_dgs1250.mld_snooping_mrouter:
    vlan_id: 1
    type: forbidden
    interface_id: eth1/0/2

- name: Disable dynamic learning on VLAN 4
  jaydee_io.dlink_dgs1250.mld_snooping_mrouter:
    vlan_id: 4
    type: learn-pimv6
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


def _build_commands(vlan_id, type_, interface_id, state):
    prefix = "no " if state == "absent" else ""
    if type_ == "learn-pimv6":
        cmd = "%sipv6 mld snooping mrouter learn pimv6" % prefix
    elif type_ == "forbidden":
        cmd = "%sipv6 mld snooping mrouter forbidden interface %s" % (
            prefix, interface_id)
    else:
        cmd = "%sipv6 mld snooping mrouter interface %s" % (
            prefix, interface_id)
    return ["vlan %d" % vlan_id, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_id=dict(type="int", required=True),
            type=dict(type="str", required=True, choices=[
                      "interface", "forbidden", "learn-pimv6"]),
            interface_id=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["vlan_id"], module.params["type"], module.params["interface_id"], module.params["state"])
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
