#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_spanning_tree_mst
short_description: Display MSTP information on a D-Link DGS-1250 switch
description:
  - Executes the C(show spanning-tree mst) CLI command on a D-Link DGS-1250 switch.
  - Displays MSTP configuration, instance, interface, or digest information.
  - Corresponds to CLI command described in chapter 46-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.15.0"
author:
  - Jérôme Dumesnil
options:
  configuration:
    description:
      - Display MST configuration mapping.
    type: bool
    default: false
  digest:
    description:
      - Display the MD5 digest of the MST configuration.
    type: bool
    default: false
  detail:
    description:
      - Display detailed information.
    type: bool
    default: false
  instance:
    description:
      - The MST instance ID to display (e.g. C(0), C(1-3)).
    type: str
  interface:
    description:
      - The interface ID to display (e.g. C(eth1/0/1), C(eth1/0/1-4)).
    type: str
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display MSTP summary
  jaydee_io.dlink_dgs1250.show_spanning_tree_mst:
  register: result

- name: Display MSTP configuration mapping
  jaydee_io.dlink_dgs1250.show_spanning_tree_mst:
    configuration: true
  register: result

- name: Display MSTP instance 2 on ports 3-4
  jaydee_io.dlink_dgs1250.show_spanning_tree_mst:
    instance: "2"
    interface: "eth1/0/3-4"
  register: result

- name: Display MSTP detailed information
  jaydee_io.dlink_dgs1250.show_spanning_tree_mst:
    detail: true
  register: result
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
        run_command,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(configuration, digest, instance, interface, detail):
    if configuration:
        cmd = "show spanning-tree mst configuration"
        if digest:
            cmd += " digest"
        return cmd
    cmd = "show spanning-tree mst"
    if instance is not None:
        cmd += " instance %s" % instance
    if interface is not None:
        cmd += " interface %s" % interface
    if detail:
        cmd += " detail"
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            configuration=dict(type="bool", default=False),
            digest=dict(type="bool", default=False),
            detail=dict(type="bool", default=False),
            instance=dict(type="str"),
            interface=dict(type="str"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(
        module.params["configuration"],
        module.params["digest"],
        module.params["instance"],
        module.params["interface"],
        module.params["detail"],
    )
    if module.check_mode:
        module.exit_json(changed=False, commands=[command], raw_output="")
        return
    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=False, raw_output=raw_output, commands=[command])


if __name__ == "__main__":
    main()
