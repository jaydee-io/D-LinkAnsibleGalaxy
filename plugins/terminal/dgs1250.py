# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
---
name: dgs1250
short_description: Terminal plugin for D-Link DGS-1250 series switches
description:
  - Terminal plugin to handle prompt detection, pagination, and error patterns
    for D-Link DGS-1250 series CLI sessions.
version_added: "0.2.0"
"""

import re

from ansible.plugins.terminal import TerminalBase
from ansible.errors import AnsibleConnectionFailure


class TerminalModule(TerminalBase):

    terminal_stdout_re = [
        re.compile(rb"[\r\n]?[\w\-]+[>#]\s*$"),
    ]

    terminal_stderr_re = [
        re.compile(rb"% ?(Error|Invalid|Incomplete|Ambiguous)"),
        re.compile(rb"% ?Bad "),
        re.compile(rb"(?:Next possible completions|Available command)"),
    ]

    def on_open_shell(self):
        try:
            self._exec_cli_command(b"disable clipaging")
        except AnsibleConnectionFailure:
            pass

    def on_become(self, passwd=None):
        prompt = self._get_prompt()
        if prompt and prompt.strip().endswith(b">"):
            cmd = {
                "command": "enable",
                "prompt": rb"[Pp]assword:",
                "answer": passwd or "",
                "prompt_retry_check": True,
            }
            try:
                self._exec_cli_command(
                    cmd["command"].encode(),
                    cmd["prompt"],
                    cmd["answer"].encode(),
                )
                prompt = self._get_prompt()
                if prompt and prompt.strip().endswith(b">"):
                    raise AnsibleConnectionFailure(
                        "Failed to escalate privilege on D-Link DGS-1250"
                    )
            except AnsibleConnectionFailure as e:
                raise AnsibleConnectionFailure(
                    "unable to elevate privilege to enable mode: %s" % e.message
                )

    def on_unbecome(self):
        prompt = self._get_prompt()
        if prompt and prompt.strip().endswith(b"#"):
            self._exec_cli_command(b"disable")
