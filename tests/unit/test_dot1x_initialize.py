"""Unit tests for dot1x_initialize module command builder."""

from dot1x_initialize import _build_commands


def test_single_interface():
    cmds = _build_commands(["eth1/0/1"], None)
    assert cmds == ["dot1x initialize interface eth1/0/1"]


def test_multiple_interfaces():
    cmds = _build_commands(["eth1/0/1", "eth1/0/5"], None)
    assert cmds == [
        "dot1x initialize interface eth1/0/1",
        "dot1x initialize interface eth1/0/5",
    ]


def test_range():
    cmds = _build_commands(["eth1/0/1-eth1/0/8"], None)
    assert cmds == ["dot1x initialize interface eth1/0/1-eth1/0/8"]


def test_mac_address():
    cmds = _build_commands(None, "00-11-22-33-44-55")
    assert cmds == ["dot1x initialize mac-address 00-11-22-33-44-55"]
