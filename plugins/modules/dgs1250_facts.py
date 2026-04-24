#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_facts
short_description: Collect facts from a D-Link DGS-1250 switch and expose them as ansible_facts
description:
  - Gathers system information from a D-Link DGS-1250 switch by executing
    multiple CLI commands and returning all parsed data as C(ansible_facts).
  - Collects version, model, serial number, uptime, memory usage, CPU utilization,
    fan/temperature/power status, interface status, VLANs, and MAC address table.
  - Similar in spirit to C(ios_facts) from the Cisco IOS collection.
  - The C(gather) parameter allows selecting which subsets of facts to collect.
  - All facts are exposed under C(ansible_facts.dgs1250) for use in subsequent tasks.
version_added: "1.2.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  gather:
    description:
      - List of fact subsets to collect.
      - If omitted or set to C([all]), all subsets are gathered.
    type: list
    elements: str
    choices: [all, version, unit, environment, cpu, interfaces, vlans, mac_table]
    default: [all]
notes:
  - This command runs in User/Privileged EXEC Mode.
  - Facts are returned both as top-level return values and under C(ansible_facts.dgs1250).
"""

EXAMPLES = r"""
- name: Gather all facts
  jaydee_io.dlink_dgs1250.dgs1250_facts:
  register: facts

- name: Display switch model and firmware
  ansible.builtin.debug:
    msg: "{{ ansible_facts.dgs1250.version.module_name }} running {{ ansible_facts.dgs1250.version.runtime }}"

- name: Gather only version and CPU utilization
  jaydee_io.dlink_dgs1250.dgs1250_facts:
    gather:
      - version
      - cpu
  register: facts

- name: Fail if CPU is too high
  jaydee_io.dlink_dgs1250.dgs1250_facts:
    gather: [cpu]
  register: facts
  failed_when: facts.cpu.five_minutes_percent > 90

- name: List all VLANs
  jaydee_io.dlink_dgs1250.dgs1250_facts:
    gather: [vlans]

- name: Check interface status
  jaydee_io.dlink_dgs1250.dgs1250_facts:
    gather: [interfaces]

- name: Use facts in conditional tasks
  jaydee_io.dlink_dgs1250.dgs1250_facts:
    gather: [version, unit]

- name: Conditional on firmware version
  ansible.builtin.debug:
    msg: "Firmware is up to date"
  when: ansible_facts.dgs1250.version.runtime == "2.04.P003"
"""

RETURN = r"""
commands:
  description: List of CLI commands sent to the switch.
  returned: always
  type: list
  elements: str
ansible_facts:
  description: Facts returned under ansible_facts.dgs1250.
  returned: always
  type: dict
  contains:
    dgs1250:
      description: All gathered facts keyed by subset name.
      type: dict
version:
  description: Version information (MAC address, model, hardware revision, firmware).
  returned: when 'version' or 'all' is in gather
  type: dict
  contains:
    system_mac_address:
      description: System MAC address.
      type: str
    module_name:
      description: Model name of the switch.
      type: str
    hardware_version:
      description: Hardware revision.
      type: str
    runtime:
      description: Runtime firmware version.
      type: str
unit:
  description: Unit information (model, serial number, uptime, memory).
  returned: when 'unit' or 'all' is in gather
  type: dict
  contains:
    model:
      description: Model information.
      type: dict
    unit:
      description: Unit status (serial number, status, uptime).
      type: dict
    memory:
      description: Memory usage for DRAM and FLASH.
      type: list
      elements: dict
environment:
  description: Environment status (fans, temperatures, power modules).
  returned: when 'environment' or 'all' is in gather
  type: dict
  contains:
    temperatures:
      description: Temperature sensor readings.
      type: list
      elements: dict
    fans:
      description: Fan status.
      type: list
      elements: dict
    power:
      description: Power module status.
      type: list
      elements: dict
cpu:
  description: CPU utilization percentages.
  returned: when 'cpu' or 'all' is in gather
  type: dict
  contains:
    five_seconds_percent:
      description: CPU utilization over the last 5 seconds.
      type: int
    one_minute_percent:
      description: CPU utilization over the last 1 minute.
      type: int
    five_minutes_percent:
      description: CPU utilization over the last 5 minutes.
      type: int
interfaces:
  description: List of interface status entries.
  returned: when 'interfaces' or 'all' is in gather
  type: list
  elements: dict
  contains:
    port:
      description: Interface name.
      type: str
    status:
      description: Link status (connected, not-connected, disabled).
      type: str
    vlan:
      description: Access VLAN ID.
      type: str
    duplex:
      description: Duplex mode (auto, full, half).
      type: str
    speed:
      description: Port speed (auto, 10M, 100M, 1000M, 10G).
      type: str
    type:
      description: Port media type (1000BASE-T, 10GBASE-SR, etc.).
      type: str
vlans:
  description: List of configured VLANs.
  returned: when 'vlans' or 'all' is in gather
  type: list
  elements: dict
  contains:
    vlan_id:
      description: VLAN ID.
      type: int
    name:
      description: VLAN name.
      type: str
    tagged_ports:
      description: Tagged member ports.
      type: str
    untagged_ports:
      description: Untagged member ports.
      type: str
mac_table:
  description: List of MAC address table entries.
  returned: when 'mac_table' or 'all' is in gather
  type: list
  elements: dict
  contains:
    vlan:
      description: VLAN ID.
      type: int
    mac_address:
      description: MAC address.
      type: str
    type:
      description: Entry type (Static, Dynamic).
      type: str
    port:
      description: Forwarding port.
      type: str
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import (
        run_command,
    )
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250_parsers import (
        parse_version, parse_unit, parse_environment, parse_cpu,
        parse_interfaces, parse_vlans, parse_mac_table,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command
    from dgs1250_parsers import (
        parse_version, parse_unit, parse_environment, parse_cpu,
        parse_interfaces, parse_vlans, parse_mac_table,
    )


# ---------------------------------------------------------------------------
# CLI commands for each subset
# ---------------------------------------------------------------------------

ALL_SUBSETS = ["version", "unit", "environment", "cpu",
               "interfaces", "vlans", "mac_table"]

SUBSET_COMMANDS = {
    "version": "show version",
    "unit": "show unit",
    "environment": "show environment",
    "cpu": "show cpu utilization",
    "interfaces": "show interfaces status",
    "vlans": "show vlan",
    "mac_table": "show mac-address-table",
}


def _build_commands(gather):
    """Return the list of CLI commands to run based on the requested subsets."""
    if "all" in gather:
        subsets = list(ALL_SUBSETS)
    else:
        subsets = [s for s in ALL_SUBSETS if s in gather]
    return subsets, [SUBSET_COMMANDS[s] for s in subsets]


_PARSERS = {
    "version": parse_version,
    "unit": parse_unit,
    "environment": parse_environment,
    "cpu": parse_cpu,
    "interfaces": parse_interfaces,
    "vlans": parse_vlans,
    "mac_table": parse_mac_table,
}


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            gather=dict(
                type="list",
                elements="str",
                default=["all"],
                choices=["all", "version", "unit", "environment", "cpu",
                         "interfaces", "vlans", "mac_table"],
            ),
        ),
        supports_check_mode=True,
    )

    gather = module.params["gather"]
    subsets, commands = _build_commands(gather)

    if module.check_mode:
        module.exit_json(changed=False, commands=commands)
        return

    result = dict(changed=False, commands=commands)
    facts = {}
    for subset, command in zip(subsets, commands):
        try:
            raw_output = run_command(module, command)
        except Exception as e:
            module.fail_json(msg="Command '%s' failed: %s" % (command, str(e)))
        parsed = _PARSERS[subset](raw_output)
        result[subset] = parsed
        facts[subset] = parsed

    result["ansible_facts"] = {"dgs1250": facts}
    module.exit_json(**result)


if __name__ == "__main__":
    main()
