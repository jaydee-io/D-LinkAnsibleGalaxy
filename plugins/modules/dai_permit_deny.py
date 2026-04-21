#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dai_permit_deny
short_description: Add a permit or deny ARP entry in an ARP access list on a D-Link DGS-1250 switch
description:
  - Configures the C(permit) or C(deny) CLI command within an ARP access list on a D-Link DGS-1250 switch.
  - Adds or removes a permit or deny ARP entry in the specified ARP access list.
  - Corresponds to CLI command described in chapter 25-11 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  acl_name:
    description:
      - The ARP access list name to configure.
    type: str
    required: true
  action:
    description:
      - C(permit) to allow, C(deny) to drop matching ARP packets.
    type: str
    choices: [permit, deny]
    required: true
  ip_any:
    description:
      - Match any source IP address.
    type: bool
    default: false
  ip_host:
    description:
      - Match a single source IP address.
    type: str
  ip_address:
    description:
      - Match a group of source IP addresses (network address).
    type: str
  ip_mask:
    description:
      - Bitmap mask for ip_address matching.
    type: str
  mac_any:
    description:
      - Match any source MAC address.
    type: bool
    default: false
  mac_host:
    description:
      - Match a single source MAC address.
    type: str
  mac_address:
    description:
      - Match a group of source MAC addresses.
    type: str
  mac_mask:
    description:
      - Bitmap mask for mac_address matching.
    type: str
  state:
    description:
      - C(present) to add, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in ARP Access-list Configuration Mode.
"""

EXAMPLES = r"""
- name: Permit IP subnet with any MAC in ARP ACL
  jaydee_io.dlink_dgs1250.dai_permit_deny:
    acl_name: static-arp-list
    action: permit
    ip_address: 10.20.0.0
    ip_mask: 255.255.0.0
    mac_any: true

- name: Remove permit entry
  jaydee_io.dlink_dgs1250.dai_permit_deny:
    acl_name: static-arp-list
    action: permit
    ip_address: 10.20.0.0
    ip_mask: 255.255.0.0
    mac_any: true
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


def _build_commands(acl_name, action, ip_any, ip_host, ip_address, ip_mask,
                    mac_any, mac_host, mac_address, mac_mask, state):
    """Build the CLI command list."""
    if ip_any:
        ip_part = "ip any"
    elif ip_host:
        ip_part = "ip host %s" % ip_host
    else:
        ip_part = "ip %s %s" % (ip_address, ip_mask)

    if mac_any:
        mac_part = "mac any"
    elif mac_host:
        mac_part = "mac host %s" % mac_host
    else:
        mac_part = "mac %s %s" % (mac_address, mac_mask)

    if state == "absent":
        cmd = "no %s %s %s" % (action, ip_part, mac_part)
    else:
        cmd = "%s %s %s" % (action, ip_part, mac_part)

    return ["arp access-list %s" % acl_name, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            acl_name=dict(type="str", required=True),
            action=dict(type="str", choices=["permit", "deny"], required=True),
            ip_any=dict(type="bool", default=False),
            ip_host=dict(type="str"),
            ip_address=dict(type="str"),
            ip_mask=dict(type="str"),
            mac_any=dict(type="bool", default=False),
            mac_host=dict(type="str"),
            mac_address=dict(type="str"),
            mac_mask=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["acl_name"],
        module.params["action"],
        module.params["ip_any"],
        module.params["ip_host"],
        module.params["ip_address"],
        module.params["ip_mask"],
        module.params["mac_any"],
        module.params["mac_host"],
        module.params["mac_address"],
        module.params["mac_mask"],
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
