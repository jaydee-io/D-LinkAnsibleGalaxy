#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: snmp_server_group
short_description: Configure an SNMP group on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server group) CLI command on a D-Link DGS-1250 switch.
  - Creates or removes an SNMP group with specified security model and views.
  - Corresponds to CLI command described in chapter 60-18 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil
options:
  group:
    description:
      - Group name (max 32 characters, no spaces).
    type: str
    required: true
  version:
    description:
      - SNMP version / security model.
    type: str
    required: true
    choices: [v1, v2c, v3-auth, v3-noauth, v3-priv]
  read_view:
    description:
      - Read-view name.
    type: str
  write_view:
    description:
      - Write-view name.
    type: str
  notify_view:
    description:
      - Notify-view name.
    type: str
  access_list:
    description:
      - Standard IP ACL name to associate with the group.
    type: str
  state:
    description:
      - C(present) to create, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Create SNMPv3 auth group
  jaydee_io.dlink_dgs1250.snmp_server_group:
    group: guestgroup
    version: v3-auth
    read_view: interfacesMibView

- name: Remove group
  jaydee_io.dlink_dgs1250.snmp_server_group:
    group: guestgroup
    version: v3-auth
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


VERSION_MAP = {
    "v1": "v1",
    "v2c": "v2c",
    "v3-auth": "v3 auth",
    "v3-noauth": "v3 noauth",
    "v3-priv": "v3 priv",
}


def _build_commands(group, version, read_view, write_view, notify_view, access_list, state):
    ver = VERSION_MAP[version]
    if state == "absent":
        return ["no snmp-server group %s %s" % (group, ver)]
    cmd = "snmp-server group %s %s" % (group, ver)
    if read_view:
        cmd += " read %s" % read_view
    if write_view:
        cmd += " write %s" % write_view
    if notify_view:
        cmd += " notify %s" % notify_view
    if access_list:
        cmd += " access %s" % access_list
    return [cmd]



def main():
    module = AnsibleModule(
        argument_spec=dict(
            group=dict(type="str", required=True),
            version=dict(type="str", required=True, choices=["v1", "v2c", "v3-auth", "v3-noauth", "v3-priv"]),
            read_view=dict(type="str"),
            write_view=dict(type="str"),
            notify_view=dict(type="str"),
            access_list=dict(type="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["group"], module.params["version"],
        module.params["read_view"], module.params["write_view"],
        module.params["notify_view"], module.params["access_list"], module.params["state"])
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
