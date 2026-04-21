#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: lldp_med_tlv_select
short_description: Configure LLDP-MED TLVs on a D-Link DGS-1250 switch interface
description:
  - Configures the C(lldp med-tlv-select) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables LLDP-MED TLVs on an interface.
  - Corresponds to CLI command described in chapter 41-8 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - "Jérôme Dumesnil (@jaydee-io)"
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  tlv_type:
    description:
      - The LLDP-MED TLV type to configure.
      - If not specified, all LLDP-MED TLVs are selected or deselected.
    type: str
    choices: [capabilities, inventory-management, network-policy, power-management]
  state:
    description:
      - C(enabled) to select the TLV, C(disabled) to deselect it.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable LLDP-MED Capabilities TLV
  jaydee_io.dlink_dgs1250.lldp_med_tlv_select:
    interface: eth1/0/1
    tlv_type: capabilities

- name: Disable all LLDP-MED TLVs
  jaydee_io.dlink_dgs1250.lldp_med_tlv_select:
    interface: eth1/0/1
    state: disabled
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


def _build_commands(interface, tlv_type, state):
    prefix = "no " if state == "disabled" else ""
    if tlv_type:
        cmd = "%slldp med-tlv-select %s" % (prefix, tlv_type)
    else:
        cmd = "%slldp med-tlv-select" % prefix
    return ["interface %s" % interface, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            tlv_type=dict(type="str", choices=[
                          "capabilities", "inventory-management", "network-policy", "power-management"]),
            state=dict(type="str", choices=[
                       "enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"], module.params["tlv_type"], module.params["state"])
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
