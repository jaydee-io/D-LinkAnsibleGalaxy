#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: snmp_server_host
short_description: Configure an SNMP notification recipient on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server host) CLI command on a D-Link DGS-1250 switch.
  - Specifies the recipient of SNMP notifications.
  - Corresponds to CLI command described in chapter 60-19 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  host:
    description:
      - IPv4 or IPv6 address of the notification host.
    type: str
    required: true
  version:
    description:
      - SNMP version for the trap.
    type: str
    choices: ["1", "2c", "3-auth", "3-noauth", "3-priv"]
  community:
    description:
      - Community string (or SNMPv3 username). Required when C(state=present).
    type: str
  port:
    description:
      - UDP port number (1-65535, default 162).
    type: int
  state:
    description:
      - C(present) to create, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Add trap host with v1
  jaydee_io.dlink_dgs1250.snmp_server_host:
    host: 163.10.50.126
    version: "1"
    community: comaccess

- name: Add trap host with v3 auth
  jaydee_io.dlink_dgs1250.snmp_server_host:
    host: 163.10.50.126
    version: "3-auth"
    community: useraccess

- name: Remove trap host
  jaydee_io.dlink_dgs1250.snmp_server_host:
    host: 163.10.50.126
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


HOST_VERSION_MAP = {
    "1": "1",
    "2c": "2c",
    "3-auth": "3 auth",
    "3-noauth": "3 noauth",
    "3-priv": "3 priv",
}


def _build_commands(host, version, community, port, state):
    if state == "absent":
        cmd = "no snmp-server host %s" % host
        if community:
            cmd += " %s" % community
        return [cmd]
    cmd = "snmp-server host %s" % host
    if version:
        cmd += " version %s" % HOST_VERSION_MAP[version]
    cmd += " %s" % community
    if port is not None:
        cmd += " port %d" % port
    return [cmd]



def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(type="str", required=True),
            version=dict(type="str", choices=["1", "2c", "3-auth", "3-noauth", "3-priv"]),
            community=dict(type="str"),
            port=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["community"])],
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["host"], module.params["version"],
        module.params["community"], module.params["port"], module.params["state"])
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
