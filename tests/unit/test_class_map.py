"""Unit tests for class_map module command builder."""

from class_map import _build_commands


def test_class_map_match_all():
    assert _build_commands("class_home_user", "match-all", "present") == [
        "class-map match-all class_home_user",
        "exit",
    ]


def test_class_map_no_match_type():
    assert _build_commands("cos", None, "present") == [
        "class-map cos",
        "exit",
    ]


def test_class_map_absent():
    assert _build_commands("cos", None, "absent") == [
        "no class-map cos",
    ]
