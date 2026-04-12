#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ddm_transceiver_monitoring_tx_power
short_description: Configure transceiver monitoring TX power thresholds on a D-Link DGS-1250 switch
description:
  - Configures the C(transceiver-monitoring tx-power) CLI command on a D-Link DGS-1250 switch.
  - Sets or removes the output power threshold for a specified SFP/SFP+ port.
  - Corresponds to CLI command described in chapter 21-8 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/25)).
    type: str
    required: true
  threshold_level:
    description:
      - C(high) or C(low) threshold level.
    type: str
    choices: [high, low]
    required: true
  threshold_type:
    description:
      - C(alarm) or C(warning) threshold type.
    type: str
    choices: [alarm, warning]
    required: true
  unit:
    description:
      - C(mwatt) for milliwatts (0 to 6.5535), C(dbm) for dBm (-40 to 8.1647).
      - Required when state is C(present).
    type: str
    choices: [mwatt, dbm]
  value:
    description:
      - The threshold value.
      - Required when state is C(present).
    type: float
  state:
    description:
      - C(present) to set, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set TX power low warning threshold in mwatt
  jaydee_io.dlink_dgs1250.ddm_transceiver_monitoring_tx_power:
    interface: eth1/0/25
    threshold_level: low
    threshold_type: warning
    unit: mwatt
    value: 0.181

- name: Remove TX power low warning threshold
  jaydee_io.dlink_dgs1250.ddm_transceiver_monitoring_tx_power:
    interface: eth1/0/25
    threshold_level: low
    threshold_type: warning
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
        run_commands, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(interface, threshold_level, threshold_type, unit, value, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no transceiver-monitoring tx-power %s %s %s" % (
            interface, threshold_level, threshold_type)]
    else:
        return ["transceiver-monitoring tx-power %s %s %s %s %s" % (
            interface, threshold_level, threshold_type, unit, value)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            threshold_level=dict(type="str", choices=["high", "low"], required=True),
            threshold_type=dict(type="str", choices=["alarm", "warning"], required=True),
            unit=dict(type="str", choices=["mwatt", "dbm"]),
            value=dict(type="float"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["unit", "value"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["threshold_level"],
        module.params["threshold_type"],
        module.params["unit"],
        module.params["value"],
        module.params["state"],
    )
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
