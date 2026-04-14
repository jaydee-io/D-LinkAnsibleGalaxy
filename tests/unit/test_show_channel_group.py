"""Unit tests for show_channel_group module."""

from show_channel_group import _build_command


def test_summary():
    assert _build_command("summary", None) == "show channel-group"


def test_detail():
    assert _build_command("detail", None) == "show channel-group channel detail"


def test_detail_channel():
    assert _build_command("detail", 3) == "show channel-group channel 3 detail"


def test_neighbor():
    assert _build_command("neighbor", None) == "show channel-group channel neighbor"


def test_neighbor_channel():
    assert _build_command("neighbor", 3) == "show channel-group channel 3 neighbor"


def test_load_balance():
    assert _build_command("load-balance", None) == "show channel-group load-balance"


def test_sys_id():
    assert _build_command("sys-id", None) == "show channel-group sys-id"
