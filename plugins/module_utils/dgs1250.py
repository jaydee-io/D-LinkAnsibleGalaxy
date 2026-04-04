"""
Common utilities for D-Link DGS-1250 Ansible modules.
Provides helpers for sending CLI commands via ansible.netcommon network_cli.
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.connection import Connection


def get_connection(module):
    """Return a Connection object bound to the module's socket path."""
    return Connection(module._socket_path)


def run_command(module, command):
    """Send a single CLI command and return its output as a string."""
    connection = get_connection(module)
    return connection.get(command)


def run_commands(module, commands):
    """Send multiple CLI commands and return their combined output."""
    connection = get_connection(module)
    output = ""
    for cmd in commands:
        output += connection.get(cmd) + "\n"
    return output
