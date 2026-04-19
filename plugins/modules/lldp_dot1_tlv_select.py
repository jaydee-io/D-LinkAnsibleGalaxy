#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: lldp_dot1_tlv_select
short_description: Configure IEEE 802.1 LLDP TLVs on a D-Link DGS-1250 switch interface
description:
  - Configures the C(lldp dot1-tlv-select) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables IEEE 802.1 Organizationally Specific TLVs for LLDP on an interface.
  - Corresponds to CLI command described in chapter 41-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - Jerome Dumesnil
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  tlv_type:
    description:
      - The TLV type to configure.
      - C(port-vlan) configures Port VLAN ID TLV.
      - C(vlan-name) configures VLAN Name TLV (requires C(vlan_id)).
      - C(protocol-identity) configures Protocol Identity TLV (optional C(protocol_name)).
    type: str
    required: true
    choices: [port-vlan, vlan-name, protocol-identity]
  vlan_id:
    description:
      - The VLAN ID for the vlan-name TLV. Required when C(tlv_type=vlan-name).
    type: str
  protocol_name:
    description:
      - The protocol name for protocol-identity TLV. Optional.
      - Choices are C(eapol), C(lacp), C(stp).
    type: str
    choices: [eapol, lacp, stp]
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
- name: Enable Port VLAN ID TLV on interface
  jaydee_io.dlink_dgs1250.lldp_dot1_tlv_select:
    interface: eth1/0/1
    tlv_type: port-vlan

- name: Enable VLAN Name TLV for VLANs 1-3 on interface
  jaydee_io.dlink_dgs1250.lldp_dot1_tlv_select:
    interface: eth1/0/1
    tlv_type: vlan-name
    vlan_id: "1-3"

- name: Enable LACP Protocol Identity TLV
  jaydee_io.dlink_dgs1250.lldp_dot1_tlv_select:
    interface: eth1/0/1
    tlv_type: protocol-identity
    protocol_name: lacp

- name: Disable Port VLAN ID TLV on interface
  jaydee_io.dlink_dgs1250.lldp_dot1_tlv_select:
    interface: eth1/0/1
    tlv_type: port-vlan
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
        run_commands, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(interface, tlv_type, vlan_id, protocol_name, state):
    prefix = "no " if state == "disabled" else ""
    if tlv_type == "port-vlan":
        cmd = "%slldp dot1-tlv-select port-vlan" % prefix
    elif tlv_type == "vlan-name":
        cmd = "%slldp dot1-tlv-select vlan-name %s" % (prefix, vlan_id)
    else:
        if protocol_name:
            cmd = "%slldp dot1-tlv-select protocol-identity %s" % (
                prefix, protocol_name)
        else:
            cmd = "%slldp dot1-tlv-select protocol-identity" % prefix
    return ["interface %s" % interface, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            tlv_type=dict(type="str", required=True, choices=[
                          "port-vlan", "vlan-name", "protocol-identity"]),
            vlan_id=dict(type="str"),
            protocol_name=dict(type="str", choices=["eapol", "lacp", "stp"]),
            state=dict(type="str", choices=[
                       "enabled", "disabled"], default="enabled"),
        ),
        required_if=[
            ("tlv_type", "vlan-name", ["vlan_id"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["interface"], module.params["tlv_type"],
                               module.params["vlan_id"], module.params["protocol_name"], module.params["state"])
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
