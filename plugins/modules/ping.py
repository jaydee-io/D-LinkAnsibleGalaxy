#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ping
short_description: Ping a remote host from a D-Link DGS-1250 switch
description:
  - Executes the C(ping) CLI command on a D-Link DGS-1250 switch.
  - Diagnoses basic network connectivity to a remote host using IPv4 or IPv6.
  - Corresponds to CLI command described in chapter 36-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.13.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  destination:
    description:
      - The destination IP address (IPv4 or IPv6) or hostname to ping.
    type: str
    required: true
  ip_version:
    description:
      - C(ip) forces IPv4, C(ipv6) forces IPv6.
      - If not specified, the switch auto-detects the address type.
    type: str
    choices: [ip, ipv6]
  count:
    description:
      - Number of echo request packets to send.
    type: int
  timeout:
    description:
      - Response timeout value in seconds.
    type: int
  source:
    description:
      - Source IP address to use for the ping packet.
    type: str
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Ping a host
  jaydee_io.dlink_dgs1250.ping:
    destination: 211.21.180.1
  register: result

- name: Ping with count and timeout
  jaydee_io.dlink_dgs1250.ping:
    destination: 211.21.180.1
    count: 4
    timeout: 5

- name: Ping an IPv6 address
  jaydee_io.dlink_dgs1250.ping:
    destination: "2001:238:f8a:77:7c10:41c0:6ddd:ecab"
    ip_version: ipv6
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
        run_commands, MODE_PRIVILEGED,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


def _build_commands(destination, ip_version, count, timeout, source):
    """Build the CLI command list."""
    cmd = "ping"
    if ip_version:
        cmd += " %s" % ip_version
    cmd += " %s" % destination
    if count is not None:
        cmd += " count %d" % count
    if timeout is not None:
        cmd += " timeout %d" % timeout
    if source:
        cmd += " source %s" % source
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            destination=dict(type="str", required=True),
            ip_version=dict(type="str", choices=["ip", "ipv6"]),
            count=dict(type="int"),
            timeout=dict(type="int"),
            source=dict(type="str"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["destination"],
        module.params["ip_version"],
        module.params["count"],
        module.params["timeout"],
        module.params["source"],
    )
    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_PRIVILEGED)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
