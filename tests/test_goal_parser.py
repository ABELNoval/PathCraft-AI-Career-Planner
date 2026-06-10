"""Tests del traductor heuristico de metas."""

from src.llm.goal_parser import parse_goal
from src.utils.data_loader import load_skills


def test_parse_goal_by_role_alias() -> None:
    parsed = parse_goal("Quiero ser Data Scientist", load_skills())

    assert parsed["goal_skill_id"] == "skill_12"
    assert parsed["confidence"] == 1.0


def test_parse_goal_by_explicit_skill_id() -> None:
    parsed = parse_goal("Necesito alcanzar skill_09", load_skills())

    assert parsed["goal_skill_id"] == "skill_09"


def test_parse_goal_by_numbered_spanish_skill() -> None:
    parsed = parse_goal("Llegar a la habilidad 12", load_skills())

    assert parsed["goal_skill_id"] == "skill_12"


def test_parse_unknown_goal_returns_empty_formal_goal() -> None:
    parsed = parse_goal("Quiero ser astronauta submarino", load_skills())

    assert parsed["goal_skill_id"] == ""
    assert parsed["confidence"] == 0.0
