#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dot1x_show
short_description: Display 802.1X configuration on a D-Link DGS-1250 switch
description:
  - Executes the C(show dot1x) CLI command on a D-Link DGS-1250 switch.
  - Returns the global 802.1X configuration or interface-specific configuration.
  - Corresponds to CLI command described in chapter 3-12 of the DGS-1250 CLI Reference Guide.
version_added: "0.2.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - Physical port interface to query (e.g. C(eth1/0/1)).
      - If omitted, global 802.1X configuration is returned.
    type: str
notes:
  - This module requires C(ansible_network_os=dlink.dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
"""

EXAMPLES = r"""
- name: Get global 802.1X configuration
  dlink.dgs1250.dot1x_show:
  register: dot1x_global

- name: Get 802.1X configuration on port 1
  dlink.dgs1250.dot1x_show:
    interface: eth1/0/1
  register: dot1x_port
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
global_config:
  description: Global 802.1X configuration (returned when no interface is specified).
  returned: when interface is not specified
  type: dict
  contains:
    dot1x_state:
      description: Whether 802.1X is enabled.
      type: bool
      sample: true
    trap_state:
      description: Whether 802.1X trap is enabled.
      type: bool
      sample: true
interface_config:
  description: Interface-specific 802.1X configuration.
  returned: when interface is specified
  type: dict
  contains:
    interface:
      description: Interface name.
      type: str
      sample: "eth1/0/1"
    pae:
      description: PAE role.
      type: str
      sample: "Authenticator"
    control_direction:
      description: Control direction.
      type: str
      sample: "Both"
    port_control:
      description: Port control mode.
      type: str
      sample: "Auto"
    tx_period:
      description: Tx period in seconds.
      type: int
      sample: 30
    supp_timeout:
      description: Supplicant timeout in seconds.
      type: int
      sample: 30
    server_timeout:
      description: Server timeout in seconds.
      type: int
      sample: 30
    max_req:
      description: Maximum request retransmissions.
      type: int
      sample: 2
    forward_pdu:
      description: Whether PDU forwarding is enabled.
      type: bool
      sample: false
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.dlink.dgs1250.plugins.module_utils.dgs1250 import run_command
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


# ---------------------------------------------------------------------------
# Output parsers
# ---------------------------------------------------------------------------

def _parse_global(output):
    """
    Parse global show dot1x output.

    Expected format:
        802.1X       : Enabled
        Trap State   : Enabled
    """
    result = {"dot1x_state": False, "trap_state": False}
    for line in output.splitlines():
        m = re.match(r"^\s*802\.1X\s*:\s*(.+?)\s*$", line)
        if m:
            result["dot1x_state"] = m.group(1).strip().lower() == "enabled"
            continue
        m = re.match(r"^\s*Trap State\s*:\s*(.+?)\s*$", line)
        if m:
            result["trap_state"] = m.group(1).strip().lower() == "enabled"
            continue
    return result


def _parse_int(value):
    """Extract integer from a string like '30 sec' or '2 times'."""
    m = re.match(r"(\d+)", value.strip())
    return int(m.group(1)) if m else 0


def _parse_interface(output):
    """
    Parse interface show dot1x output.

    Expected format:
        Interface        : eth1/0/1
        PAE              : Authenticator
        Control Direction : Both
        Port Control     : Auto
        Tx Period        : 30 sec
        Supp Timeout     : 30 sec
        Server Timeout   : 30 sec
        Max-req          : 2 times
        Forward PDU      : Disabled
    """
    result = {
        "interface": "",
        "pae": "",
        "control_direction": "",
        "port_control": "",
        "tx_period": 0,
        "supp_timeout": 0,
        "server_timeout": 0,
        "max_req": 0,
        "forward_pdu": False,
    }

    field_map = {
        "Interface": ("interface", str),
        "PAE": ("pae", str),
        "Control Direction": ("control_direction", str),
        "Port Control": ("port_control", str),
        "Tx Period": ("tx_period", _parse_int),
        "Supp Timeout": ("supp_timeout", _parse_int),
        "Server Timeout": ("server_timeout", _parse_int),
        "Max-req": ("max_req", _parse_int),
        "Forward PDU": ("forward_pdu", lambda v: v.strip().lower() == "enabled"),
    }

    for line in output.splitlines():
        m = re.match(r"^\s*(.+?)\s*:\s*(.+?)\s*$", line)
        if m:
            key = m.group(1).strip()
            value = m.group(2).strip()
            if key in field_map:
                field_name, converter = field_map[key]
                result[field_name] = converter(value)

    return result


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
        ),
        supports_check_mode=True,
    )

    interface = module.params["interface"]

    command = "show dot1x"
    if interface:
        command += " interface %s" % interface

    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    result = dict(changed=False, raw_output=raw_output)

    if interface:
        result["interface_config"] = _parse_interface(raw_output)
    else:
        result["global_config"] = _parse_global(raw_output)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
