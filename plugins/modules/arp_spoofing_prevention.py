#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: arp_spoofing_prevention
short_description: Configure ARP spoofing prevention on a D-Link DGS-1250 switch
description:
  - Configures the C(ip arp spoofing-prevention) CLI command on a D-Link DGS-1250 switch.
  - Creates or removes an ARP Spoofing Prevention entry to protect against ARP poisoning attacks.
  - Corresponds to CLI command described in chapter 6-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.5.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  gateway_ip:
    description:
      - IP address of the gateway to protect.
    type: str
    required: true
  gateway_mac:
    description:
      - MAC address of the gateway. Required when C(state=present).
    type: str
  interface:
    description:
      - Interface or list of interfaces on which to activate the entry (e.g. C(eth1/0/10)).
    type: str
    required: true
  state:
    description:
      - C(present) to create the entry, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Add ARP spoofing prevention entry
  jaydee_io.dlink_dgs1250.arp_spoofing_prevention:
    gateway_ip: 10.254.254.251
    gateway_mac: 00-00-00-11-11-11
    interface: eth1/0/10

- name: Remove ARP spoofing prevention entry
  jaydee_io.dlink_dgs1250.arp_spoofing_prevention:
    gateway_ip: 10.254.254.251
    interface: eth1/0/10
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


def _build_commands(gateway_ip, gateway_mac, interface, state):
    if state == "absent":
        return ["no ip arp spoofing-prevention %s interface %s" % (gateway_ip, interface)]
    return ["ip arp spoofing-prevention %s %s interface %s" % (gateway_ip, gateway_mac, interface)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            gateway_ip=dict(type="str", required=True),
            gateway_mac=dict(type="str"),
            interface=dict(type="str", required=True),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["gateway_mac"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["gateway_ip"],
        module.params["gateway_mac"],
        module.params["interface"],
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
