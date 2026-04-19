#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: aaa_show_tacacs_statistics
short_description: Display TACACS+ statistics on a D-Link DGS-1250 switch
description:
  - Executes the C(show tacacs statistics) CLI command on a D-Link DGS-1250 switch.
  - Returns parsed TACACS+ server statistics for all configured servers.
  - Corresponds to CLI command described in chapter 8-29 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options: {}
"""

EXAMPLES = r"""
- name: Show TACACS+ statistics
  jaydee_io.dlink_dgs1250.aaa_show_tacacs_statistics:
  register: tacacs_stats
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
servers:
  description: List of TACACS+ server statistics.
  returned: always
  type: list
  elements: dict
  contains:
    server:
      description: Server IP address.
      type: str
    port:
      description: TCP port.
      type: int
    state:
      description: Server state (Up or Down).
      type: str
    socket_opens:
      description: Number of socket opens.
      type: int
    socket_closes:
      description: Number of socket closes.
      type: int
    total_packets_sent:
      description: Total packets sent.
      type: int
    total_packets_recv:
      description: Total packets received.
      type: int
    reference_count:
      description: Reference count.
      type: int
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import run_command
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


# ---------------------------------------------------------------------------
# Output parser
# ---------------------------------------------------------------------------

def _parse_tacacs_stats(output):
    """Parse show tacacs statistics output."""
    servers = []
    current = None

    field_map = {
        "Socket Opens": ("socket_opens", int),
        "Socket Closes": ("socket_closes", int),
        "Total Packets Sent": ("total_packets_sent", int),
        "Total Packets Recv": ("total_packets_recv", int),
        "Reference Count": ("reference_count", int),
    }

    for line in output.splitlines():
        m = re.match(
            r"^\s*TACACS\+?\s+Server:\s*(.+?)/(\d+),\s*State is (\w+)", line)
        if m:
            current = {
                "server": m.group(1).strip(),
                "port": int(m.group(2)),
                "state": m.group(3).strip(),
                "socket_opens": 0,
                "socket_closes": 0,
                "total_packets_sent": 0,
                "total_packets_recv": 0,
                "reference_count": 0,
            }
            servers.append(current)
            continue

        if current is None:
            continue

        m = re.match(r"^\s*(.+?)\s*:\s*(.+?)\s*$", line)
        if m:
            key = m.group(1).strip()
            value = m.group(2).strip()
            if key in field_map:
                field_name, converter = field_map[key]
                try:
                    current[field_name] = converter(value)
                except (ValueError, TypeError):
                    current[field_name] = value

    return servers


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True,
    )

    try:
        raw_output = run_command(module, "show tacacs statistics")
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    servers = _parse_tacacs_stats(raw_output)
    module.exit_json(changed=False, raw_output=raw_output, servers=servers)


if __name__ == "__main__":
    main()
