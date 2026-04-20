#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: lldp_dot3_tlv_select
short_description: Configure IEEE 802.3 LLDP TLVs on a D-Link DGS-1250 switch interface
description:
  - Configures the C(lldp dot3-tlv-select) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables IEEE 802.3 Organizationally Specific TLVs for LLDP on an interface.
  - Corresponds to CLI command described in chapter 41-4 of the DGS-1250 CLI Reference Guide.
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
      - The TLV type to configure.
    type: str
    choices: [mac-phy-cfg, link-aggregation, power, max-frame-size]
  state:
    description:
      - C(enabled) to select the TLV, C(disabled) to deselect it.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Interface Configuration Mode.
  - If C(tlv_type) is not specified, all 802.3 TLVs are selected or deselected.
"""

EXAMPLES = r"""
- name: Enable MAC/PHY Configuration/Status TLV
  jaydee_io.dlink_dgs1250.lldp_dot3_tlv_select:
    interface: eth1/0/1
    tlv_type: mac-phy-cfg

- name: Disable all 802.3 TLVs on interface
  jaydee_io.dlink_dgs1250.lldp_dot3_tlv_select:
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
        run_commands, is_config_present, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, MODE_GLOBAL_CONFIG


def _build_commands(interface, tlv_type, state):
    prefix = "no " if state == "disabled" else ""
    if tlv_type:
        cmd = "%slldp dot3-tlv-select %s" % (prefix, tlv_type)
    else:
        cmd = "%slldp dot3-tlv-select" % prefix
    return ["interface %s" % interface, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            tlv_type=dict(type="str", choices=[
                          "mac-phy-cfg", "link-aggregation", "power", "max-frame-size"]),
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
