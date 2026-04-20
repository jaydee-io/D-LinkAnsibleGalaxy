#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dai_ip_arp_inspection_validate
short_description: Configure ARP inspection validation checks on a D-Link DGS-1250 switch
description:
  - Configures the C(ip arp inspection validate) CLI command on a D-Link DGS-1250 switch.
  - Specifies additional checks to perform during ARP inspection.
  - Corresponds to CLI command described in chapter 25-8 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  src_mac:
    description:
      - Enable source MAC address validation.
    type: bool
    default: false
  dst_mac:
    description:
      - Enable destination MAC address validation.
    type: bool
    default: false
  ip:
    description:
      - Enable IP address validation.
    type: bool
    default: false
  state:
    description:
      - C(present) to configure, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable source MAC validation
  jaydee_io.dlink_dgs1250.dai_ip_arp_inspection_validate:
    src_mac: true

- name: Enable all validations
  jaydee_io.dlink_dgs1250.dai_ip_arp_inspection_validate:
    src_mac: true
    dst_mac: true
    ip: true

- name: Remove src-mac validation
  jaydee_io.dlink_dgs1250.dai_ip_arp_inspection_validate:
    src_mac: true
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


def _build_commands(src_mac, dst_mac, ip, state):
    """Build the CLI command list."""
    opts = []
    if src_mac:
        opts.append("src-mac")
    if dst_mac:
        opts.append("dst-mac")
    if ip:
        opts.append("ip")
    cmd_opts = " ".join(opts)
    if state == "absent":
        cmd = "no ip arp inspection validate"
        if cmd_opts:
            cmd += " " + cmd_opts
    else:
        cmd = "ip arp inspection validate"
        if cmd_opts:
            cmd += " " + cmd_opts
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            src_mac=dict(type="bool", default=False),
            dst_mac=dict(type="bool", default=False),
            ip=dict(type="bool", default=False),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["src_mac"],
        module.params["dst_mac"],
        module.params["ip"],
        module.params["state"],
    )
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
