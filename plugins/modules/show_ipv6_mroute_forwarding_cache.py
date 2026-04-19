#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_ipv6_mroute_forwarding_cache
short_description: Display IPv6 multicast forwarding cache on a D-Link DGS-1250 switch
description:
  - Executes the C(show ipv6 mroute forwarding-cache) CLI command on a D-Link DGS-1250 switch.
  - Displays the contents of the IPv6 multicast routing forwarding cache database.
  - Corresponds to CLI command described in chapter 34-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.12.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  group_addr:
    description:
      - Optional IPv6 address of the multicast group to filter by.
    type: str
  source_addr:
    description:
      - Optional IPv6 address of the multicast source to filter by.
      - Can only be specified together with C(group_addr).
    type: str
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display all IPv6 multicast forwarding cache
  jaydee_io.dlink_dgs1250.show_ipv6_mroute_forwarding_cache:
  register: result

- name: Display IPv6 multicast forwarding cache for a group
  jaydee_io.dlink_dgs1250.show_ipv6_mroute_forwarding_cache:
    group_addr: "FF0E::1:1:1"
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(group_addr, source_addr):
    cmd = "show ipv6 mroute forwarding-cache"
    if group_addr:
        cmd += " group-addr %s" % group_addr
        if source_addr:
            cmd += " source-addr %s" % source_addr
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            group_addr=dict(type="str"),
            source_addr=dict(type="str"),
        ),
        required_by={"source_addr": "group_addr"},
        supports_check_mode=True,
    )
    command = _build_command(
        module.params["group_addr"], module.params["source_addr"])
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
