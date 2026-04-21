#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dai_ip_arp_inspection_vlan_logging
short_description: Configure ARP inspection logging for a VLAN on a D-Link DGS-1250 switch
description:
  - Configures the C(ip arp inspection vlan logging) CLI command on a D-Link DGS-1250 switch.
  - Controls the type of packets that are logged during ARP inspection.
  - Corresponds to CLI command described in chapter 25-10 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  vlan_id:
    description:
      - The VLAN ID or range to configure logging (e.g. C(1) or C(1-10)).
    type: str
    required: true
  log_type:
    description:
      - "The logging criteria type: C(acl-match) or C(dhcp-bindings)."
      - Required when state is C(present).
    type: str
    choices: [acl-match, dhcp-bindings]
  log_action:
    description:
      - The logging action. C(permit) logs permitted packets, C(all) logs all, C(none) disables logging.
      - Required when state is C(present).
    type: str
    choices: [permit, all, none]
  state:
    description:
      - C(present) to configure, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Log ACL-matched packets on VLAN 1
  jaydee_io.dlink_dgs1250.dai_ip_arp_inspection_vlan_logging:
    vlan_id: "1"
    log_type: acl-match
    log_action: all

- name: Revert logging to default on VLAN 1
  jaydee_io.dlink_dgs1250.dai_ip_arp_inspection_vlan_logging:
    vlan_id: "1"
    log_type: acl-match
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
        run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG


def _build_commands(vlan_id, log_type, log_action, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no ip arp inspection vlan %s logging %s" % (vlan_id, log_type)]
    else:
        return ["ip arp inspection vlan %s logging %s %s" % (vlan_id, log_type, log_action)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_id=dict(type="str", required=True),
            log_type=dict(type="str", choices=["acl-match", "dhcp-bindings"]),
            log_action=dict(type="str", choices=["permit", "all", "none"]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["log_type", "log_action"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["vlan_id"],
        module.params["log_type"],
        module.params["log_action"],
        module.params["state"],
    )
    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
    diff = build_config_diff(module, commands) if module._diff else None
    if module.check_mode:
        result = dict(changed=True, commands=commands, raw_output="")
        if diff:
            result['diff'] = diff
        module.exit_json(**result)
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    result = dict(changed=True, raw_output=raw_output, commands=commands)
    if diff:
        result['diff'] = diff
    module.exit_json(**result)


if __name__ == "__main__":
    main()
