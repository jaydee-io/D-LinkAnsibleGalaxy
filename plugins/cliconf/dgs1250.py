# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
---
name: dgs1250
short_description: Cliconf plugin for D-Link DGS-1250 series switches
description:
  - Cliconf plugin to send CLI commands and retrieve output
    from D-Link DGS-1250 series switches via network_cli.
version_added: "0.2.0"
"""

from ansible.plugins.cliconf import CliconfBase


class Cliconf(CliconfBase):

    def get_device_info(self):
        device_info = {}
        device_info["network_os"] = "jaydee_io.dlink_dgs1250.dgs1250"

        reply = self.get("show version")
        if reply:
            for line in reply.splitlines():
                if "Module Name" in line:
                    device_info["network_os_model"] = line.split()[-1]
                elif "Runtime" in line:
                    device_info["network_os_version"] = line.split()[-1]
                elif "H/W" in line:
                    device_info["network_os_hardware"] = line.split()[-1]

        return device_info

    def get_config(self, source="running", flags=None):
        if source == "running":
            cmd = "show running-config"
        elif source == "startup":
            cmd = "show startup-config"
        else:
            return self.invalid_params(
                "fetching configuration from %s is not supported" % source
            )
        if flags:
            cmd += " " + " ".join(flags)
        return self.send_command(cmd)

    def edit_config(self, candidate=None, commit=True, replace=None, comment=None):
        responses = []
        for cmd in candidate:
            responses.append(self.send_command(cmd))
        return responses

    def get(self, command, prompt=None, answer=None, sendonly=False, newline=True, check_all=False):
        return self.send_command(
            command=command,
            prompt=prompt,
            answer=answer,
            sendonly=sendonly,
            newline=newline,
            check_all=check_all,
        )

    def get_capabilities(self):
        return {
            "rpc": [
                "get_config",
                "edit_config",
                "get",
                "get_capabilities",
                "get_device_info",
            ],
            "network_api": "cliconf",
            "device_info": self.get_device_info(),
        }
