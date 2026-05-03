"""Unit tests for dgs1250_config module helper functions."""

from dgs1250_config import _section_lines, _filter_lines, _build_commands, _normalize_parents


# ---------------------------------------------------------------------------
# _normalize_parents
# ---------------------------------------------------------------------------

def test_normalize_parents_none():
    assert _normalize_parents(None) == []


def test_normalize_parents_string():
    assert _normalize_parents("interface eth1/0/1") == ["interface eth1/0/1"]


def test_normalize_parents_list():
    assert _normalize_parents(["interface eth1/0/1", "vlan 10"]) == [
        "interface eth1/0/1", "vlan 10"]


# ---------------------------------------------------------------------------
# _section_lines
# ---------------------------------------------------------------------------

SAMPLE_CONFIG = """\
hostname switch01
!
interface eth1/0/1
 description Uplink
 switchport mode trunk
 no shutdown
!
interface eth1/0/2
 description Server
 switchport mode access
 switchport access vlan 100
!
vlan 100
 name management
!
"""


def test_section_lines_no_parents_returns_all():
    section = _section_lines(SAMPLE_CONFIG, [])
    assert "hostname switch01" in section
    assert "interface eth1/0/1" in section
    assert "description Uplink" in section


def test_section_lines_under_interface():
    section = _section_lines(SAMPLE_CONFIG, ["interface eth1/0/1"])
    assert "description Uplink" in section
    assert "switchport mode trunk" in section
    assert "no shutdown" in section
    # Lines from another interface are not included
    assert "description Server" not in section
    assert "switchport access vlan 100" not in section


def test_section_lines_under_other_interface():
    section = _section_lines(SAMPLE_CONFIG, ["interface eth1/0/2"])
    assert "description Server" in section
    assert "switchport access vlan 100" in section
    # Lines from another interface are not included
    assert "no shutdown" not in section


def test_section_lines_under_vlan():
    section = _section_lines(SAMPLE_CONFIG, ["vlan 100"])
    assert "name management" in section


def test_section_lines_missing_parent():
    section = _section_lines(SAMPLE_CONFIG, ["interface eth1/0/99"])
    assert section == set()


def test_section_lines_empty_config():
    assert _section_lines("", ["interface eth1/0/1"]) == set()


# ---------------------------------------------------------------------------
# _filter_lines
# ---------------------------------------------------------------------------

def test_filter_lines_match_none_returns_all():
    lines = ["description Uplink", "shutdown"]
    result = _filter_lines(lines, ["interface eth1/0/1"], SAMPLE_CONFIG, "none")
    assert result == lines


def test_filter_lines_match_line_filters_existing():
    lines = ["description Uplink", "description New", "shutdown"]
    result = _filter_lines(lines, ["interface eth1/0/1"], SAMPLE_CONFIG, "line")
    # 'description Uplink' is already present, 'shutdown' is "no shutdown" so different
    assert "description Uplink" not in result
    assert "description New" in result
    assert "shutdown" in result


def test_filter_lines_no_running_config_returns_all():
    lines = ["description X"]
    result = _filter_lines(lines, ["interface eth1/0/1"], None, "line")
    assert result == lines


def test_filter_lines_empty_lines():
    assert _filter_lines([], ["interface eth1/0/1"], SAMPLE_CONFIG, "line") == []
    assert _filter_lines(None, ["interface eth1/0/1"], SAMPLE_CONFIG, "line") == []


def test_filter_lines_all_present_returns_empty():
    lines = ["description Uplink", "switchport mode trunk", "no shutdown"]
    result = _filter_lines(lines, ["interface eth1/0/1"], SAMPLE_CONFIG, "line")
    assert result == []


# ---------------------------------------------------------------------------
# _build_commands
# ---------------------------------------------------------------------------

def test_build_commands_lines_only():
    cmds = _build_commands([], [], ["hostname switch01"], [])
    assert cmds == ["hostname switch01"]


def test_build_commands_with_parents():
    cmds = _build_commands(
        [], ["interface eth1/0/1"], ["description Uplink", "shutdown"], [])
    assert cmds == ["interface eth1/0/1",
                    "description Uplink", "shutdown", "exit"]


def test_build_commands_no_lines_to_apply_skips_parents():
    cmds = _build_commands([], ["interface eth1/0/1"], [], [])
    assert cmds == []


def test_build_commands_before_after():
    cmds = _build_commands(
        ["banner motd ^test^"], ["interface eth1/0/1"],
        ["description X"], ["end"])
    assert cmds == [
        "banner motd ^test^",
        "interface eth1/0/1",
        "description X",
        "exit",
        "end",
    ]


def test_build_commands_only_before():
    cmds = _build_commands(["banner motd ^test^"], [], [], [])
    assert cmds == ["banner motd ^test^"]


def test_build_commands_multiple_parents():
    cmds = _build_commands(
        [], ["vlan 100", "name management"], ["state active"], [])
    # All parents are emitted; followed by lines and a single exit.
    assert cmds == ["vlan 100", "name management",
                    "state active", "exit"]
