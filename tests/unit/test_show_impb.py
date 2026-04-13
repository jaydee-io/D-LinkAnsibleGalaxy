"""Unit tests for show_impb module."""

from show_impb import _build_command


def test_no_params():
    assert _build_command(None, False) == "show ip ip-mac-port-binding"


def test_interface():
    assert _build_command("eth1/0/3", False) == "show ip ip-mac-port-binding interface eth1/0/3"


def test_violation():
    assert _build_command(None, True) == "show ip ip-mac-port-binding violation"


def test_interface_violation():
    assert _build_command("eth1/0/3", True) == (
        "show ip ip-mac-port-binding interface eth1/0/3 violation"
    )
