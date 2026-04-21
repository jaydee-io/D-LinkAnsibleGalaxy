#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_nd_prefix
short_description: Configure IPv6 ND prefix on an interface of a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 nd prefix) CLI command on a D-Link DGS-1250 switch.
  - Configures IPv6 prefixes to be advertised in router advertisements on a specific interface.
  - Corresponds to CLI command described in chapter 10-9 of the DGS-1250 CLI Reference Guide.
version_added: "0.7.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface on which to configure the ND prefix (e.g. C(vlan1)).
    type: str
    required: true
  ipv6_prefix:
    description:
      - IPv6 prefix to advertise.
    type: str
    required: true
  prefix_length:
    description:
      - Prefix length for the IPv6 prefix.
    type: int
    required: true
  valid_lifetime:
    description:
      - Valid lifetime in seconds. Must be specified together with C(preferred_lifetime).
    type: int
  preferred_lifetime:
    description:
      - Preferred lifetime in seconds. Must be specified together with C(valid_lifetime).
    type: int
  off_link:
    description:
      - When C(true), indicate that the prefix is off-link.
    type: bool
    default: false
  no_autoconfig:
    description:
      - When C(true), indicate that the prefix should not be used for autoconfiguration.
    type: bool
    default: false
  state:
    description:
      - C(present) to configure the prefix, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Configure an ND prefix on vlan1
  jaydee_io.dlink_dgs1250.ipv6_nd_prefix:
    interface: vlan1
    ipv6_prefix: "2001:db8::"
    prefix_length: 64

- name: Configure an ND prefix with lifetimes
  jaydee_io.dlink_dgs1250.ipv6_nd_prefix:
    interface: vlan1
    ipv6_prefix: "2001:db8::"
    prefix_length: 64
    valid_lifetime: 2592000
    preferred_lifetime: 604800

- name: Configure an ND prefix with off-link and no-autoconfig
  jaydee_io.dlink_dgs1250.ipv6_nd_prefix:
    interface: vlan1
    ipv6_prefix: "2001:db8::"
    prefix_length: 64
    off_link: true
    no_autoconfig: true

- name: Remove an ND prefix
  jaydee_io.dlink_dgs1250.ipv6_nd_prefix:
    interface: vlan1
    ipv6_prefix: "2001:db8::"
    prefix_length: 64
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


def _build_commands(interface, ipv6_prefix, prefix_length, valid_lifetime,
                    preferred_lifetime, off_link, no_autoconfig, state):
    """Build the CLI command list."""
    if state == "absent":
        cmd = "no ipv6 nd prefix %s/%d" % (ipv6_prefix, prefix_length)
    else:
        cmd = "ipv6 nd prefix %s/%d" % (ipv6_prefix, prefix_length)
        if valid_lifetime is not None and preferred_lifetime is not None:
            cmd += " %d %d" % (valid_lifetime, preferred_lifetime)
        if off_link:
            cmd += " off-link"
        if no_autoconfig:
            cmd += " no-autoconfig"
    return ["interface %s" % interface, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            ipv6_prefix=dict(type="str", required=True),
            prefix_length=dict(type="int", required=True),
            valid_lifetime=dict(type="int"),
            preferred_lifetime=dict(type="int"),
            off_link=dict(type="bool", default=False),
            no_autoconfig=dict(type="bool", default=False),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_together=[
            ("valid_lifetime", "preferred_lifetime"),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"],
        module.params["ipv6_prefix"],
        module.params["prefix_length"],
        module.params["valid_lifetime"],
        module.params["preferred_lifetime"],
        module.params["off_link"],
        module.params["no_autoconfig"],
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
