"""Unit tests for voice_vlan_mode module."""

from voice_vlan_mode import _build_commands


def test_auto_tag():
    assert _build_commands("eth1/0/1", "auto_tag", "present") == [
        "interface eth1/0/1", "voice vlan mode auto tag", "exit"]


def test_auto_untag():
    assert _build_commands("eth1/0/1", "auto_untag", "present") == [
        "interface eth1/0/1", "voice vlan mode auto untag", "exit"]


def test_manual():
    assert _build_commands("eth1/0/1", "manual", "present") == [
        "interface eth1/0/1", "voice vlan mode manual", "exit"]


def test_absent():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1", "no voice vlan mode", "exit"]
